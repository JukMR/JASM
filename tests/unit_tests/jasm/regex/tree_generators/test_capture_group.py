import pytest

from jasm.global_definitions import IGNORE_INST_ADDR, CaptureGroupMode
from jasm.regex.tree_generators.capture_group import CaptureGroupIndex

from unittest.mock import Mock


# Setup Mock PatternNode
@pytest.fixture
def mock_pattern_node():
    node = Mock()
    node.name = "1"
    node.root_node.capture_group_references = ["1", "2", "3"]
    return node


# Testing Initialization


def test_initialization_with_valid_node(mock_pattern_node):
    cgi = CaptureGroupIndex(mock_pattern_node, CaptureGroupMode.instruction)
    assert cgi.index == 1
    assert cgi.mode == CaptureGroupMode.instruction


def test_initialization_without_capture_group_references(mock_pattern_node):
    mock_pattern_node.root_node.capture_group_references = None
    with pytest.raises(AssertionError):
        CaptureGroupIndex(mock_pattern_node, CaptureGroupMode.instruction)


def test_get_capture_group_reference_valid():
    references = ["1", "2", "3"]
    index = CaptureGroupIndex._get_capture_group_reference("2", references)
    assert index == 2


# Testing _get_capture_group_reference Static Method


def test_get_capture_group_reference_not_found():
    references = ["1", "2", "3"]
    with pytest.raises(ValueError):
        CaptureGroupIndex._get_capture_group_reference("4", references)


# Testing to_regex Method
def test_to_regex_instruction(mock_pattern_node):
    cgi = CaptureGroupIndex(mock_pattern_node, CaptureGroupMode.instruction)
    expected_regex = rf"{IGNORE_INST_ADDR}\{cgi.index},\|"
    assert cgi.to_regex() == expected_regex


def test_to_regex_operand(mock_pattern_node):
    cgi = CaptureGroupIndex(mock_pattern_node, CaptureGroupMode.operand)
    expected_regex = rf"\{cgi.index}"
    assert cgi.to_regex() == expected_regex


def test_to_regex_unsupported_mode(mock_pattern_node):
    cgi = CaptureGroupIndex(mock_pattern_node, "unsupported_mode")  # type: ignore
    with pytest.raises(ValueError):
        cgi.to_regex()
