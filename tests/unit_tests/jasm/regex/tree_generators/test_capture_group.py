from unittest.mock import Mock

from jasm.regex.tree_generators.capture_manager import CapturesManager
from jasm.regex.tree_generators.shared_context import SharedContext
import pytest

from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.capture_group_index import (
    CaptureGroupIndexInstructionCall,
    CaptureGroupIndexOperandCall,
)


# Setup Mock SharedContext
@pytest.fixture
def mock_shared_context() -> SharedContext:
    shared_context = SharedContext(CapturesManager())
    shared_context.capture_manager.add_capture("1")
    shared_context.capture_manager.add_capture("2")
    shared_context.capture_manager.add_capture("3")
    return shared_context


# Setup Mock PatternNode
@pytest.fixture
def mock_pattern_node(mock_shared_context: SharedContext):
    node = Mock()
    node.name = "1"
    node.shared_context = mock_shared_context
    return node


# Testing Initialization


def test_initialization_with_valid_node(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexInstructionCall(mock_pattern_node)
    assert cgi.index == 1
    assert isinstance(cgi, CaptureGroupIndexInstructionCall)


def test_initialization_without_capture_group_references(mock_pattern_node) -> None:
    shared_context = SharedContext(CapturesManager())
    mock_pattern_node.shared_context = shared_context

    with pytest.raises(ValueError):
        CaptureGroupIndexInstructionCall(mock_pattern_node)


# Testing to_regex Method
def test_to_regex_instruction(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexInstructionCall(mock_pattern_node)
    expected_regex = rf"{IGNORE_INST_ADDR}\{cgi.index},\|"
    assert cgi.to_regex() == expected_regex


def test_to_regex_operand(mock_pattern_node) -> None:
    cgi = CaptureGroupIndexOperandCall(mock_pattern_node)
    expected_regex = rf"\{cgi.index}"
    assert cgi.to_regex() == expected_regex
