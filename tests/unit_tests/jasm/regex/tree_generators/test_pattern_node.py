# test_pattern_node_definition
from typing import List
from unittest.mock import MagicMock

import pytest

from jasm.global_definitions import IGNORE_NAME_PREFIX, IGNORE_NAME_SUFFIX, PatternNodeTypes, ASTERISK_WITH_LIMIT
from jasm.regex.tree_generators.pattern_node import (
    BranchProcessor,
    PatternNode,
    RegexWithOperandsCreator,
    TimeType,
    get_pattern_node_name,
)


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
def pattern_node_fixture():
    # Create a basic pattern_node fixture
    return PatternNode(
        pattern_node_dict={},
        name="test",
        times=TimeType(min_times=1, max_times=1),
        children=[],
        pattern_node_type=PatternNodeTypes.operand,
        parent=None,
        root_node=None,
    )


def test_get_regex_mnemonic(pattern_node_fixture: PatternNode) -> None:
    pattern_node_fixture.pattern_node_type = PatternNodeTypes.mnemonic
    pattern_node_fixture.process_leaf = MagicMock(return_value="leaf_regex")
    assert pattern_node_fixture.get_regex(pattern_node_fixture) == "leaf_regex"
    pattern_node_fixture.process_leaf.assert_called_once()


def test_get_regex_operand(pattern_node_fixture: PatternNode) -> None:
    pattern_node_fixture.pattern_node_type = PatternNodeTypes.operand
    pattern_node_fixture.process_leaf = MagicMock(return_value="leaf_regex")
    assert pattern_node_fixture.get_regex(pattern_node_fixture) == "leaf_regex"
    pattern_node_fixture.process_leaf.assert_called_once()


def test_process_leaf_no_children(pattern_node_fixture: PatternNode):
    pattern_node_fixture.name = "operand"
    pattern_node_fixture.pattern_node_type = PatternNodeTypes.operand
    pattern_node_fixture.children = None
    # Assuming sanitize_operand_name works correctly
    assert (
        pattern_node_fixture.process_leaf(pattern_node_fixture) == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX
    )


def test_process_leaf_with_children(pattern_node_fixture: PatternNode):
    pattern_node_fixture.name = "pattern_node_with_children"
    pattern_node_fixture.pattern_node_type = PatternNodeTypes.mnemonic
    child_pattern_node = PatternNode(
        pattern_node_dict={},
        name="child",
        times=TimeType(min_times=1, max_times=1),
        children=None,
        pattern_node_type=PatternNodeTypes.operand,
        parent=pattern_node_fixture,
        root_node=pattern_node_fixture,
    )
    pattern_node_fixture.children = [child_pattern_node]
    # Assuming generate_regex works correctly
    assert "pattern_node_with_children" in pattern_node_fixture.process_leaf(pattern_node_fixture)


def test_sanitize_operand_name_hex(pattern_node_fixture: PatternNode):
    hex_name = "A3h"
    assert pattern_node_fixture.sanitize_operand_name(hex_name) == "0xA3"


def test_sanitize_operand_name_non_hex(pattern_node_fixture: PatternNode) -> None:
    non_hex_name = "operand"
    assert (
        pattern_node_fixture.sanitize_operand_name(non_hex_name) == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX
    )


def test_process_branch_and(pattern_node_fixture: PatternNode):
    # Create mock pattern_node instances for children
    mock_child1 = MagicMock(spec=PatternNode)
    mock_child2 = MagicMock(spec=PatternNode)

    # Manually set up necessary attributes for the mock children
    for i_mock, mock_child in enumerate([mock_child1, mock_child2]):
        mock_child.name = f"mock_child{i_mock + 1}"
        mock_child.times = TimeType(min_times=1, max_times=1)
        mock_child.children = []
        mock_child.pattern_node_type = PatternNodeTypes.operand
        mock_child.get_regex = MagicMock(return_value=f"{mock_child.name}")

    # Set up the return value for get_regex method on mock children
    mock_child1.get_regex.return_value = "child1_regex"
    mock_child2.get_regex.return_value = "child2_regex"

    # Assign these mock children to the pattern_node_fixture
    pattern_node_fixture.children = [mock_child1, mock_child2]
    pattern_node_fixture.name = "$and"
    pattern_node_fixture.pattern_node_type = PatternNodeTypes.node  # or appropriate type

    regex = pattern_node_fixture.process_branch(pattern_node_fixture)

    print(mock_child1.name)
    assert (
        regex
        == f"(?:[^,|]{ASTERISK_WITH_LIMIT}mock_child1[^,|]{ASTERISK_WITH_LIMIT},[^,|]{ASTERISK_WITH_LIMIT}mock_child2[^,|]{ASTERISK_WITH_LIMIT},)"
    )

    # Optionally, you can assert that get_regex was called on the child pattern_nodes
    # mock_child1.get_regex.assert_called_once()
    # mock_child2.get_regex.assert_called_once()


def test_generate_regex_with_operands():
    creator = RegexWithOperandsCreator(name="pattern_node", operands=[MagicMock()], times=None)
    assert isinstance(creator.operands, List)
    creator.operands[0].get_regex = MagicMock(return_value="operand_regex")
    assert "operand_regex" in creator.generate_regex()


def test_generate_regex_without_operands():
    creator = RegexWithOperandsCreator(name="pattern_node", operands=None, times=None)
    assert "pattern_node" in creator.generate_regex()


from jasm.regex.tree_generators.pattern_node import BranchProcessor


def test_branch_processor_and():
    processor = BranchProcessor()
    assert processor.process_and(["regex1", "regex2"], None) == "(?:regex1regex2)"
