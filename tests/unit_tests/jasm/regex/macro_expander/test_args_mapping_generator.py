from typing import Any
import pytest

from jasm.regex.macro_expander.args_mapping_generator import ArgsMappingGenerator


@pytest.fixture
def args_mapping_generator() -> ArgsMappingGenerator:
    return ArgsMappingGenerator()


# Tests for get_args_mapping_dictx


def test_get_args_mapping_dict_simple(args_mapping_generator: ArgsMappingGenerator) -> None:
    tree = {"arg1": "value1", "arg2": "value2"}
    args = ["arg1", "arg2"]
    expected = {"arg1": "value1", "arg2": "value2"}
    assert args_mapping_generator.get_args_mapping_dict(tree, args) == expected


def test_get_args_mapping_dict_no_match(args_mapping_generator: ArgsMappingGenerator) -> None:
    tree = {"arg1": "value1"}
    args = ["arg2"]
    expected: dict[Any, Any] = {}
    assert args_mapping_generator.get_args_mapping_dict(tree, args) == expected


# Tests _get_args_mapping


def test_get_args_mapping_dict_nested(args_mapping_generator: ArgsMappingGenerator) -> None:
    tree = {"nested": {"arg1": "value1"}}
    args = ["arg1"]
    expected = {"arg1": "value1"}
    assert args_mapping_generator.get_args_mapping_dict(tree, args) == expected


def test__get_args_mapping_simple(args_mapping_generator: ArgsMappingGenerator) -> None:
    tree = "arg1"
    current_arg = "arg1"
    expected = [{"arg1": "arg1"}]
    assert list(args_mapping_generator._get_args_mapping(tree, current_arg)) == expected


def test__get_args_mapping_no_match(args_mapping_generator: ArgsMappingGenerator) -> None:
    tree = {"arg1": "value1"}
    current_arg = "arg2"
    assert list(args_mapping_generator._get_args_mapping(tree, current_arg)) == []


# Tests for _yield_key_value_pairs


def test_yield_key_value_pairs_dict(args_mapping_generator: ArgsMappingGenerator) -> None:
    data = {"key1": "value1", "key2": "value2"}
    expected = [("key1", "value1"), ("key2", "value2")]
    assert list(args_mapping_generator._yield_key_value_pairs(data)) == expected


def test_yield_key_value_pairs_nested(args_mapping_generator: ArgsMappingGenerator) -> None:
    data = {"outer": {"inner": "value"}}
    expected = [("outer", {"inner": "value"}), ("inner", "value")]
    assert list(args_mapping_generator._yield_key_value_pairs(data)) == expected
