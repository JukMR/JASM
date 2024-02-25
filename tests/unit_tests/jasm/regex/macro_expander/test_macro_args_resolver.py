import pytest
from jasm.regex.macro_expander.macro_args_resolver import MacroArgsResolver

from typing import Any


@pytest.fixture
def macro_args_resolver() -> MacroArgsResolver:
    return MacroArgsResolver()


@pytest.fixture
def sample_macro() -> dict[str, Any]:
    return {"name": "MACRO1", "args": ["arg1", "arg2"], "pattern": {"key1": "arg1", "key2": ["arg2"]}}


@pytest.fixture
def sample_tree() -> dict[str, str]:
    return {"arg1": "value1", "arg2": "value2"}


# Tests for resolve


def test_resolve(macro_args_resolver: MacroArgsResolver, sample_macro, sample_tree) -> None:
    resolved_macro = macro_args_resolver.resolve(sample_macro, sample_tree)
    assert resolved_macro["pattern"]["key1"] == "value1"
    assert resolved_macro["pattern"]["key2"] == ["value2"]


# Tests for get_macro_mapping_arg_dict


def test_get_macro_mapping_arg_dict(macro_args_resolver: MacroArgsResolver, sample_macro, sample_tree) -> None:
    mapping_dict = macro_args_resolver.get_macro_mapping_arg_dict(sample_macro, sample_tree)
    expected_dict = {"arg1": "value1", "arg2": "value2"}
    assert mapping_dict == expected_dict


# Test for evaluate_args_in_macro


def test_evaluate_args_in_macro(macro_args_resolver: MacroArgsResolver, sample_macro) -> None:
    mapping_dict = {"arg1": "value1", "arg2": "value2"}
    updated_macro = macro_args_resolver.evaluate_args_in_macro(sample_macro, mapping_dict)
    assert updated_macro["pattern"]["key1"] == "value1"
    assert updated_macro["pattern"]["key2"] == ["value2"]


# Tests for iter_items_with_path
def test_iter_items_with_path(macro_args_resolver: MacroArgsResolver) -> None:
    elems = {"key": "value", "list_key": ["list_value1", "list_value2"]}
    paths = list(macro_args_resolver.iter_items_with_path(elems))
    expected_paths = [
        (("key",), ("key", "value")),  # Initially yields the key and its value as a tuple
        (("key",), "value"),  # Then yields the value for the key
        (("list_key",), ("list_key", ["list_value1", "list_value2"])),  # Yields the key and the list as a tuple
        (("list_key", 0), "list_value1"),  # Yields the first list item with its index path
        (("list_key", 1), "list_value2"),  # Yields the second list item with its index path
    ]
    assert paths == expected_paths


# Tests for replace_item_in_structure
def test_replace_item_in_structure(macro_args_resolver: MacroArgsResolver) -> None:
    struct = {"key": "old_value"}
    path = ("key",)
    macro_args_resolver.replace_item_in_structure(struct, path, "new_value")
    assert struct["key"] == "new_value"
