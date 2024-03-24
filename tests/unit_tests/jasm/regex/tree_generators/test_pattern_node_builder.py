import pytest

from jasm.global_definitions import TimeType
from jasm.regex.tree_generators.pattern_node import PatternNodeBase
from jasm.regex.tree_generators.pattern_node_builder import PatternNodeBuilderNoParents


def test_pattern_node_builder_no_parents_with_dict():
    # Sample input representing a command dictionary
    command_dict = {"test_command": {"times": {"min": 1, "max": 3}, "operands": ["op1", "op2"]}}

    builder = PatternNodeBuilderNoParents(command_dict)

    assert builder.name == "test_command"
    assert builder.times == TimeType(min_times=1, max_times=3)
    assert isinstance(builder.children, list)
    assert len(builder.children) == 2
    assert all(isinstance(child, PatternNodeBase) for child in builder.children)
    assert all(child.name in ["times", "operands"] for child in builder.children)
    assert builder.children[0].times == TimeType(min_times=1, max_times=1)
    assert builder.children[1].times == TimeType(min_times=1, max_times=1)

    assert builder.children[1].children
    assert ["op1", "op2"] == builder.children[1].children[0].name


# Additional tests would cover other initialization paths: int, str, tuple, and edge cases.


def test_get_name():
    command_dict = {"command_name": {}}
    name = PatternNodeBuilderNoParents._get_name(command_dict)
    assert name == "command_name"


@pytest.mark.parametrize(
    "input_times, expected",
    [
        ({"min": 2, "max": 4}, TimeType(min_times=2, max_times=4)),
        ({"min": 3, "max": 3}, TimeType(min_times=3, max_times=3)),
        ({}, TimeType(min_times=1, max_times=1)),  # Testing default behavior
    ],
)
def test_get_times(input_times, expected):
    command_dict = {"command": {"times": input_times}} if isinstance(input_times, dict) else input_times
    times = PatternNodeBuilderNoParents(command_dict)._get_times(command_dict if isinstance(command_dict, dict) else {})
    assert times == expected
