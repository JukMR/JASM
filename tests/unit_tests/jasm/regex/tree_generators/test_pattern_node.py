# test_pattern_node_definition
from typing import List
from unittest.mock import MagicMock

import pytest

from jasm.global_definitions import ASTERISK_WITH_LIMIT, IGNORE_NAME_PREFIX, IGNORE_NAME_SUFFIX
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode, PatternNodeData
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterCall,
)
from jasm.regex.tree_generators.pattern_node_implementations.mnemonic_and_operand.mnemonic_and_operand import (
    PatternNodeMnemonic,
    PatternNodeOperand,
    TimeType,
    _RegexWithOperandsCreator,
    get_pattern_node_name,
)
from jasm.regex.tree_generators.pattern_node_implementations.node_branch_root import PatternNodeNode, _BranchProcessor
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.shared_context import SharedContext


def test_get_pattern_node_name_with_string():
    name = f"[^, ]{ASTERISK_WITH_LIMIT}"

    result = get_pattern_node_name("pattern_node", allow_matching_substrings=False, name_prefix="", name_suffix="")
    assert result == "pattern_node"

    result = get_pattern_node_name(
        "pattern_node", allow_matching_substrings=True, name_prefix="prefix_", name_suffix="_suffix"
    )
    assert result == "prefix_pattern_node_suffix"

    result = get_pattern_node_name(
        "@any", allow_matching_substrings=True, name_prefix=IGNORE_NAME_PREFIX, name_suffix=IGNORE_NAME_SUFFIX
    )
    assert result == f"{IGNORE_NAME_PREFIX}{name}{IGNORE_NAME_SUFFIX}"

    result = get_pattern_node_name(
        "@any", allow_matching_substrings=False, name_prefix="prefix_", name_suffix="_suffix"
    )
    assert result == name


@pytest.fixture
def pattern_node_fixture() -> PatternNodeTmpUntyped:
    # Create a basic pattern_node fixture
    return PatternNodeTmpUntyped(
        PatternNodeData(
            name="test",
            times=TimeType(min_times=1, max_times=1),
            children=[],
            parent=None,
            shared_context=SharedContext(),
        )
    )


def test_get_regex_mnemonic(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_mnemonic = PatternNodeMnemonic(pattern_node_fixture)
    pattern_node_mnemonic.process_leaf = MagicMock(return_value="leaf_regex")
    assert pattern_node_mnemonic.get_regex() == "leaf_regex"
    pattern_node_mnemonic.process_leaf.assert_called_once()


def test_get_regex_operand(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_operand = PatternNodeOperand(pattern_node_fixture)
    pattern_node_operand.process_leaf = MagicMock(return_value="leaf_regex")
    assert pattern_node_operand.get_regex() == "leaf_regex"
    pattern_node_operand.process_leaf.assert_called_once()


def test_process_leaf_no_children(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_operand = PatternNodeOperand(pattern_node_fixture)
    pattern_node_operand.name = "operand"
    pattern_node_operand.children = None
    # Assuming sanitize_operand_name works correctly
    assert pattern_node_operand.process_leaf() == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX


def test_process_leaf_with_children(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_mnemonic = PatternNodeMnemonic(pattern_node_fixture)
    pattern_node_mnemonic.name = "pattern_node_with_children"
    child_pattern_node_base = PatternNodeTmpUntyped(
        PatternNodeData(
            name="child",
            times=TimeType(min_times=1, max_times=1),
            children=None,
            parent=pattern_node_mnemonic,
            shared_context=SharedContext(),
        )
    )
    child_pattern_node = PatternNodeOperand(child_pattern_node_base)

    pattern_node_mnemonic.children = [child_pattern_node]
    # Assuming generate_regex works correctly
    assert "pattern_node_with_children" in pattern_node_mnemonic.process_leaf()


def test_sanitize_operand_name_hex(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_operand = PatternNodeOperand(pattern_node_fixture)
    hex_name = "A3h"
    assert pattern_node_operand.sanitize_operand_name(hex_name) == "0xA3"


def test_sanitize_operand_name_non_hex(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    pattern_node_operand = PatternNodeOperand(pattern_node_fixture)
    non_hex_name = "operand"
    assert (
        pattern_node_operand.sanitize_operand_name(non_hex_name) == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX
    )


def test_process_branch_and(pattern_node_fixture: PatternNodeTmpUntyped) -> None:
    # Create mock pattern_node instances for children
    mock_child1 = MagicMock(spec=PatternNode)
    mock_child2 = MagicMock(spec=PatternNode)

    # Manually set up necessary attributes for the mock children
    for i_mock, mock_child in enumerate([mock_child1, mock_child2]):
        mock_child.name = f"mock_child{i_mock + 1}"
        mock_child.times = TimeType(min_times=1, max_times=1)
        mock_child.children = []
        mock_child.get_regex = MagicMock(return_value=f"{mock_child.name}")

    # Set up the return value for get_regex method on mock children
    mock_child1.get_regex.return_value = "[^,|]{0,1000}mock_child1[^,|]{0,1000},"
    mock_child2.get_regex.return_value = "[^,|]{0,1000}mock_child2[^,|]{0,1000},"

    # Assign these mock children to the pattern_node_fixture
    pattern_node_node = PatternNodeNode(pattern_node_fixture)
    pattern_node_node.children = [mock_child1, mock_child2]
    pattern_node_node.name = "$and"

    regex = pattern_node_node.process_branch()

    print(mock_child1.name)
    assert (
        regex
        == f"(?:[^,|]{ASTERISK_WITH_LIMIT}mock_child1[^,|]{ASTERISK_WITH_LIMIT},[^,|]{ASTERISK_WITH_LIMIT}mock_child2[^,|]{ASTERISK_WITH_LIMIT},)"
    )

    # Optionally, you can assert that get_regex was called on the child pattern_nodes
    # mock_child1.get_regex.assert_called_once()
    # mock_child2.get_regex.assert_called_once()


def test_generate_regex_with_operands() -> None:
    creator = _RegexWithOperandsCreator(name="pattern_node", operands=[MagicMock()], times=None)
    assert isinstance(creator.operands, List)
    creator.operands[0].get_regex = MagicMock(return_value="operand_regex")
    assert "operand_regex" in creator.generate_regex()


def test_generate_regex_without_operands() -> None:
    creator = _RegexWithOperandsCreator(name="pattern_node", operands=None, times=None)
    assert "pattern_node" in creator.generate_regex()


def test_branch_processor_and() -> None:
    processor = _BranchProcessor()
    assert processor.process_and(["regex1", "regex2"], None) == "(?:regex1regex2)"


def test_process_register_capture_group_name():
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&genreg.64", "1") == "r1x"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&genreg.32", "2") == "e2x"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&genreg.16", "3") == "3x"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&genreg.8h", "4") == "4h"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&genreg.8l", "5") == "5l"

    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_indreg("&indreg.64", "1") == "r1i"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_indreg("&indreg.32", "2") == "e2i"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_indreg("&indreg.16", "3") == "3i"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_indreg("&indreg.8l", "4") == "4il"

    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_basereg("&basereg.64", "1") == "r1"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_basereg("&basereg.32", "2") == "e2"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_basereg("&basereg.16", "3") == "3"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_basereg("&basereg.8l", "4") == "4l"

    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_stackreg("&stackreg.64", "1") == "r1"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_stackreg("&stackreg.32", "2") == "e2"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_stackreg("&stackreg.16", "3") == "3"
    assert PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_stackreg("&stackreg.8l", "4") == "4l"

    with pytest.raises(NotImplementedError):
        PatternNodeCaptureGroupRegisterCall.process_register_capture_group_name_genreg("&pattern.unknown", "7")
