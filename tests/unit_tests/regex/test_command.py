# test_command_definition
from typing import List
from unittest.mock import MagicMock

import pytest

from jasm.regex.pattern_node import (
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    BranchProcessor,
    PatternNode,
    PatternNodeTypes,
    RegexWithOperandsCreator,
    TimeType,
    get_command_name,
)


def test_get_command_name_with_string():
    result = get_command_name("command", allow_matching_substrings=False, name_prefix="", name_suffix="")
    assert result == "command"

    result = get_command_name("command", allow_matching_substrings=True, name_prefix="prefix_", name_suffix="_suffix")
    assert result == "prefix_command_suffix"

    result = get_command_name("@any", allow_matching_substrings=True, name_prefix="prefix_", name_suffix="_suffix")
    assert result == "prefix_[^,]*_suffix"

    result = get_command_name("@any", allow_matching_substrings=False, name_prefix="prefix_", name_suffix="_suffix")
    assert result == "[^,]*"


@pytest.fixture
def command_fixture():
    # Create a basic Command fixture
    return PatternNode(
        pattern_node_dict={},
        name="test",
        times=TimeType(min_times=1, max_times=1),
        children=[],
        command_type=PatternNodeTypes.operand,
        parent=None,
    )


def test_get_regex_mnemonic(command_fixture: PatternNode) -> None:
    command_fixture.pattern_node_type = PatternNodeTypes.mnemonic
    command_fixture.process_leaf = MagicMock(return_value="leaf_regex")
    assert command_fixture.get_regex(command_fixture) == "leaf_regex"
    command_fixture.process_leaf.assert_called_once()


def test_get_regex_operand(command_fixture: PatternNode) -> None:
    command_fixture.pattern_node_type = PatternNodeTypes.operand
    command_fixture.process_leaf = MagicMock(return_value="leaf_regex")
    assert command_fixture.get_regex(command_fixture) == "leaf_regex"
    command_fixture.process_leaf.assert_called_once()


def test_process_leaf_no_children(command_fixture: PatternNode):
    command_fixture.name = "operand"
    command_fixture.pattern_node_type = PatternNodeTypes.operand
    command_fixture.children = None
    # Assuming sanitize_operand_name works correctly
    assert command_fixture.process_leaf(command_fixture) == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX


def test_process_leaf_with_children(command_fixture: PatternNode):
    command_fixture.name = "command_with_children"
    command_fixture.pattern_node_type = PatternNodeTypes.mnemonic
    child_command = PatternNode(
        pattern_node_dict={},
        name="child",
        times=TimeType(min_times=1, max_times=1),
        children=None,
        command_type=PatternNodeTypes.operand,
        parent=command_fixture,
    )
    command_fixture.children = [child_command]
    # Assuming generate_regex works correctly
    assert "command_with_children" in command_fixture.process_leaf(command_fixture)


def test_sanitize_operand_name_hex(command_fixture: PatternNode):
    hex_name = "A3h"
    assert command_fixture.sanitize_operand_name(hex_name) == "0xA3"


def test_sanitize_operand_name_non_hex(command_fixture: PatternNode) -> None:
    non_hex_name = "operand"
    assert command_fixture.sanitize_operand_name(non_hex_name) == IGNORE_NAME_PREFIX + "operand" + IGNORE_NAME_SUFFIX


def test_process_branch_and(command_fixture: PatternNode):
    # Create mock Command instances for children
    mock_child1 = MagicMock(spec=PatternNode)
    mock_child2 = MagicMock(spec=PatternNode)

    # Manually set up necessary attributes for the mock children
    for i_mock, mock_child in enumerate([mock_child1, mock_child2]):
        mock_child.name = f"mock_child{i_mock + 1}"
        mock_child.times = TimeType(min_times=1, max_times=1)
        mock_child.children = []
        mock_child.command_type = PatternNodeTypes.operand
        mock_child.get_regex = MagicMock(return_value=f"{mock_child.name}")

    # Set up the return value for get_regex method on mock children
    mock_child1.get_regex.return_value = "child1_regex"
    mock_child2.get_regex.return_value = "child2_regex"

    # Assign these mock children to the command_fixture
    command_fixture.children = [mock_child1, mock_child2]
    command_fixture.name = "$and"
    command_fixture.pattern_node_type = PatternNodeTypes.node  # or appropriate type

    regex = command_fixture.process_branch(command_fixture)

    print(mock_child1.name)
    assert regex == "([^,|]*mock_child1[^,|]*,[^,|]*mock_child2[^,|]*,)"

    # Optionally, you can assert that get_regex was called on the child commands
    # mock_child1.get_regex.assert_called_once()
    # mock_child2.get_regex.assert_called_once()


def test_generate_regex_with_operands():
    creator = RegexWithOperandsCreator(name="command", operands=[MagicMock()], times=None)
    assert isinstance(creator.operands, List)
    creator.operands[0].get_regex = MagicMock(return_value="operand_regex")
    assert "operand_regex" in creator.generate_regex()


def test_generate_regex_without_operands():
    creator = RegexWithOperandsCreator(name="command", operands=None, times=None)
    assert "command" in creator.generate_regex()


from jasm.regex.pattern_node import BranchProcessor


def test_branch_processor_and():
    processor = BranchProcessor()
    assert processor.process_and(["regex1", "regex2"], None) == "(regex1regex2)"
