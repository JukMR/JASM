import pytest

from jasm.global_definitions import TimeType, remove_access_suffix
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeTypes
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder, RegisterCaptureGroupProcessor
from src.jasm.regex.tree_generators.pattern_node import PatternNodeBase
from src.jasm.regex.tree_generators.pattern_node_implementations import (
    PatternNodeDeref,
    PatternNodeDerefProperty,
    PatternNodeMnemonic,
    PatternNodeNode,
    PatternNodeTimes,
)


def create_test_node(name: str, parent=None, children=None) -> PatternNodeBase:
    node = PatternNodeBase(
        pattern_node_dict={},
        name=name,
        times=TimeType(min_times=1, max_times=1),
        children=children or [],
        parent=parent,
        root_node=parent,
    )
    return node


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

    root_node = create_test_node("$and")
    node = create_test_node(name)
    root_node.children = [node]

    # Transform parents of all nodes to commands
    PatternNodeParentsBuilder(root_node).build()

    # Add the command_type to each node
    PatternNodeTypeBuilder(root_node, parent=None).build()

    assert isinstance(root_node.children[0], expected_type)


def test_is_ancestor_deref():
    child = create_test_node("child", parent=[], children=[])
    parent = create_test_node("$deref", parent=[], children=[child])

    PatternNodeParentsBuilder(parent).build()
    PatternNodeTypeBuilder(parent, parent=None).build()

    assert isinstance(parent, PatternNodeDeref)
    assert parent.children
    assert parent.children[0]
    assert isinstance(parent.children[0], PatternNodeDerefProperty)

    child2 = create_test_node("child2", parent=parent, children=[])

    PatternNodeParentsBuilder(child2).build()
    PatternNodeTypeBuilder(child2, parent=parent).build()

    child2_builder = PatternNodeTypeBuilder(child2, parent=parent)
    assert child2_builder.is_ancestor_deref() is True


def test_any_ancestor_is_mnemonic():
    child = create_test_node("child")
    parent = create_test_node("parent", children=[child])
    grandparent = create_test_node("mnemonic", children=[parent])
    root = create_test_node("$and", children=[grandparent])

    PatternNodeParentsBuilder(root).build()

    PatternNodeTypeBuilder(root, parent=None).build()

    child_pattern_type = PatternNodeTypeBuilder(child, parent=root)

    assert child_pattern_type.any_ancestor_is_mnemonic() is True


def test_recursive_build():
    child = create_test_node("child")
    parent = create_test_node("$deref", children=[child])
    grandparent = create_test_node("mnemonic", children=[parent])

    parent_builder = PatternNodeParentsBuilder(grandparent)
    parent_builder.build()

    builder_type = PatternNodeTypeBuilder(grandparent, parent=None)
    builder_type.build()

    type_builder = PatternNodeTypeBuilder(child, parent=parent)
    type_builder.build()
    builder = PatternNodeTypeBuilder(parent, parent=grandparent)
    builder.build()

    assert isinstance(parent, PatternNodeDeref)
    assert isinstance(child, PatternNodeDerefProperty)


def test_remove_access_suffix():
    assert remove_access_suffix("pattern.32") == "pattern"
    assert remove_access_suffix("pattern.16") == "pattern"
    assert remove_access_suffix("pattern.8l") == "pattern"
    assert remove_access_suffix("pattern.8h") == "pattern"
    assert remove_access_suffix("pattern") == "pattern"
    assert remove_access_suffix("pattern.other") == "pattern.other"
