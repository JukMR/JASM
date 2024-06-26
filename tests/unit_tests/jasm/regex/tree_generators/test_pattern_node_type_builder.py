from typing import Optional

import pytest

from jasm.global_definitions import TimesType, remove_access_suffix
from jasm.regex.tree_generators.capture_manager import CapturesManager
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode, PatternNodeData
from jasm.regex.tree_generators.pattern_node_implementations.deref import PatternNodeDeref, PatternNodeDerefProperty
from jasm.regex.tree_generators.pattern_node_implementations.mnemonic_and_operand.mnemonic_and_operand import (
    PatternNodeMnemonic,
)
from jasm.regex.tree_generators.pattern_node_implementations.node_branch_root import PatternNodeNode, PatternNodeTimes
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.pattern_node_type_builder.pattern_node_type_builder import PatternNodeTypeBuilder
from jasm.regex.tree_generators.shared_context import SharedContext


@pytest.fixture
def mock_shared_context() -> SharedContext:
    shared_context = SharedContext(CapturesManager())
    return shared_context


def pattern_node_base_creator(
    name: str | int,
    times: TimesType = TimesType(_min_times=1, _max_times=1),
    children: Optional[list[PatternNode]] = None,
    parent: Optional[PatternNode] = None,
    shared_context: SharedContext = SharedContext(CapturesManager()),
) -> PatternNode:

    pattern_node_data = PatternNodeData(
        name=name,
        times=times,
        children=children,
        parent=parent,
        shared_context=shared_context,
    )

    return PatternNodeTmpUntyped(pattern_node_data)


@pytest.mark.parametrize(
    "name, expected_type",
    [
        ("$deref", PatternNodeDeref),
        ("times", PatternNodeTimes),
        ("1", PatternNodeMnemonic),
        ("$or", PatternNodeNode),
    ],
)
def test_get_type(name: str, expected_type: PatternNode) -> None:

    root_node = pattern_node_base_creator(name="$and")

    node = pattern_node_base_creator(
        name=name,
        parent=root_node,
    )

    root_node.children = [node]

    # Add the command_type to each node
    root_node = PatternNodeTypeBuilder().build(root_node, parent=None)

    assert isinstance(root_node.children[0], expected_type)


def test_is_ancestor_deref() -> None:

    root_node = pattern_node_base_creator(name="$and")

    child = pattern_node_base_creator(name="child", parent=None)

    parent = pattern_node_base_creator(name="$deref", parent=root_node, children=[child])

    root_node.children = [parent]
    root_node = PatternNodeTypeBuilder().build(root_node, parent=None)

    parent = root_node.children[0]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert parent.children
    assert child
    assert isinstance(child, PatternNodeDerefProperty)

    child2 = pattern_node_base_creator(name="child2", parent=parent)

    child2_builder = PatternNodeTypeBuilder()
    child2 = child2_builder.build(child2, parent=parent)

    assert child2_builder.is_ancestor_deref()


def test_any_ancestor_is_mnemonic(mock_shared_context: SharedContext) -> None:
    child = pattern_node_base_creator(name="child")
    parent = pattern_node_base_creator(name="parent", children=[child])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    # pattern_node_tree_builder = PatternNodeTypeBuilder(root, parent=None)
    pattern_node_tree_builder = PatternNodeTypeBuilder()
    root = pattern_node_tree_builder.build(pattern_node=root, parent=None)
    grandparent = root.children[0]
    parent = grandparent.children[0]
    child = parent.children[0]

    child_pattern_builder = PatternNodeTypeBuilder()
    child_pattern_type = child_pattern_builder.build(child, parent=parent)

    assert child_pattern_builder.any_ancestor_is_mnemonic()


def test_recursive_build() -> None:
    child = pattern_node_base_creator(name="child")
    parent = pattern_node_base_creator(name="$deref", children=[child])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    root = PatternNodeTypeBuilder().build(pattern_node=root, parent=None)
    grandparent = root.children[0]
    parent = grandparent.children[0]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert isinstance(child, PatternNodeDerefProperty)


def test_remove_access_suffix() -> None:
    assert remove_access_suffix("pattern.32") == "pattern"
    assert remove_access_suffix("pattern.16") == "pattern"
    assert remove_access_suffix("pattern.8l") == "pattern"
    assert remove_access_suffix("pattern.8h") == "pattern"
    assert remove_access_suffix("pattern") == "pattern"
    assert remove_access_suffix("pattern.other") == "pattern.other"
