from typing import Optional
from jasm.regex.tree_generators.pattern_node_builder import PatternNodeBuilderNoParents
import pytest

from jasm.global_definitions import TimeType, remove_access_suffix
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeTypes
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder, RegisterCaptureGroupProcessor
from jasm.regex.tree_generators.pattern_node import PatternNodeBase
from jasm.regex.tree_generators.pattern_node_implementations import (
    PatternNodeDeref,
    PatternNodeDerefProperty,
    PatternNodeMnemonic,
    PatternNodeNode,
    PatternNodeRoot,
    PatternNodeTimes,
)


def pattern_node_base_creator(
    parent: Optional[PatternNodeBase] = None,
    children: list[PatternNodeBase] = [],
    root_node: Optional[PatternNodeBase] = None,
    name: str = "PatternNodeBase",
) -> PatternNodeBase:
    return PatternNodeBase(
        pattern_node_dict={},
        name=name,
        times=TimeType(min_times=1, max_times=1),
        children=children,
        parent=parent or None,
        root_node=root_node or None,
    )


@pytest.mark.parametrize(
    "name, expected_type",
    [
        ("$deref", PatternNodeDeref),
        ("times", PatternNodeTimes),
        ("1", PatternNodeMnemonic),
        ("$or", PatternNodeNode),
    ],
)
def test_get_type(name, expected_type):

    root_node = pattern_node_base_creator(name="$and")

    root_node.root_node = root_node

    node = pattern_node_base_creator(name=name, parent=root_node, root_node=root_node)

    root_node.children = [node]

    # Transform parents of all nodes to commands
    PatternNodeParentsBuilder(root_node).build()

    # Add the command_type to each node
    root_node = PatternNodeTypeBuilder(root_node, parent=None).build()

    assert isinstance(root_node.children[0], expected_type)


def test_is_ancestor_deref() -> None:

    root_node = pattern_node_base_creator(name="$and")

    child = pattern_node_base_creator(name="child", root_node=root_node)

    parent = pattern_node_base_creator(name="$deref", parent=root_node, children=[child], root_node=root_node)

    root_node.children = [parent]
    PatternNodeParentsBuilder(root_node).build()
    root_node = PatternNodeTypeBuilder(root_node, parent=None).build()

    parent = root_node.children[0]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert parent.children
    assert child
    assert isinstance(child, PatternNodeDerefProperty)

    child2 = pattern_node_base_creator(name="child2", parent=parent, root_node=root_node)

    PatternNodeParentsBuilder(child2).build()
    child2 = PatternNodeTypeBuilder(child2, parent=parent).build()

    child2_builder = PatternNodeTypeBuilder(child2, parent=parent)
    assert child2_builder.is_ancestor_deref()


def test_any_ancestor_is_mnemonic():
    child = pattern_node_base_creator(name="child")
    parent = pattern_node_base_creator(name="parent", children=[child])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    PatternNodeParentsBuilder(root).build()

    root = PatternNodeTypeBuilder(root, parent=None).build()
    grandparent = root.children[0]
    parent = grandparent.children[0]
    child = parent.children[0]

    child_pattern_type = PatternNodeTypeBuilder(child, parent=parent)

    assert child_pattern_type.any_ancestor_is_mnemonic() is True


def test_recursive_build():
    child = pattern_node_base_creator(name="child")
    parent = pattern_node_base_creator(name="$deref", children=[child])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    root_builder = PatternNodeParentsBuilder(root)
    root_builder.build()

    root = PatternNodeTypeBuilder(root, parent=None).build()
    grandparent = root.children[0]
    parent = grandparent.children[0]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert isinstance(child, PatternNodeDerefProperty)


def test_remove_access_suffix():
    assert remove_access_suffix("pattern.32") == "pattern"
    assert remove_access_suffix("pattern.16") == "pattern"
    assert remove_access_suffix("pattern.8l") == "pattern"
    assert remove_access_suffix("pattern.8h") == "pattern"
    assert remove_access_suffix("pattern") == "pattern"
    assert remove_access_suffix("pattern.other") == "pattern.other"
