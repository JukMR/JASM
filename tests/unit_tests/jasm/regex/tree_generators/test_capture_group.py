from unittest.mock import Mock

import pytest

from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.capture_group import CaptureGroupIndexInstruction, CaptureGroupIndexOperand


# Setup Mock PatternNode
@pytest.fixture
def mock_pattern_node():
    node = Mock()
    node.name = "1"
    node.root_node.capture_group_references = ["1", "2", "3"]
    return node


# Testing Initialization


def test_initialization_with_valid_node(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexInstruction(mock_pattern_node)
    assert cgi.index == 1
    assert isinstance(cgi, CaptureGroupIndexInstruction)


def test_initialization_without_capture_group_references(mock_pattern_node) -> None:
    mock_pattern_node.root_node.capture_group_references = None
    with pytest.raises(AssertionError):
        CaptureGroupIndexInstruction(mock_pattern_node)


@pytest.fixture
def dummy_capture_group_index(mock_pattern_node):
    return CaptureGroupIndexInstruction(mock_pattern_node)


def test_get_capture_group_reference_valid(dummy_capture_group_index) -> None:
    references = ["1", "2", "3"]
    index = dummy_capture_group_index._get_capture_group_reference("2", references)
    assert index == 2


# Testing _get_capture_group_reference Static Method


def test_get_capture_group_reference_not_found(dummy_capture_group_index) -> None:
    references = ["1", "2", "3"]
    with pytest.raises(ValueError):
        dummy_capture_group_index._get_capture_group_reference("4", references)


# Testing to_regex Method
def test_to_regex_instruction(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexInstruction(mock_pattern_node)
    expected_regex = rf"{IGNORE_INST_ADDR}\{cgi.index},\|"
    assert cgi.to_regex() == expected_regex


def test_to_regex_operand(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexOperand(mock_pattern_node)
    expected_regex = rf"\{cgi.index}"
    assert cgi.to_regex() == expected_regex
