import pytest

from jasm.global_definitions import TimeType
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeTypes
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder, RegisterCaptureGroupProcessor


def create_test_node(name: str, parent=None, children=None) -> PatternNode:
    node = PatternNode(
        pattern_node_dict={},
        name=name,
        times=TimeType(min_times=1, max_times=1),
        children=children or [],
        pattern_node_type=None,
        parent=parent,
        root_node=parent,
    )
    return node


@pytest.mark.parametrize(
    "name, expected_type",
    [
        ("$deref", PatternNodeTypes.deref),
        ("times", PatternNodeTypes.times),
        ("1", PatternNodeTypes.mnemonic),
        ("$or", PatternNodeTypes.node),
    ],
)
def test_get_type(name, expected_type):

    root_node = create_test_node("$and")
    node = create_test_node(name)
    root_node.children = [node]

    # Transform parents of all nodes to commands
    PatternNodeParentsBuilder(root_node).build()

    # Add the command_type to each node
    PatternNodeTypeBuilder(root_node).build()

    assert root_node.children[0].pattern_node_type == expected_type


def test_is_ancestor_deref():
    child = create_test_node("child", parent=[], children=[])
    parent = create_test_node("$deref", parent=[], children=[child])

    PatternNodeParentsBuilder(parent).build()
    PatternNodeTypeBuilder(parent).build()

    assert parent.pattern_node_type == PatternNodeTypes.deref
    assert parent.children
    assert parent.children[0]
    assert parent.children[0].pattern_node_type == PatternNodeTypes.deref_property

    child2 = create_test_node("child2", parent=parent, children=[])

    PatternNodeParentsBuilder(child2).build()
    PatternNodeTypeBuilder(child2).build()

    child2_builder = PatternNodeTypeBuilder(child2)
    assert child2_builder.is_ancestor_deref() is True


def test_any_ancestor_is_mnemonic():
    child = create_test_node("child")
    parent = create_test_node("parent", children=[child])
    grandparent = create_test_node("mnemonic", children=[parent])
    root = create_test_node("$and", children=[grandparent])

    PatternNodeParentsBuilder(root).build()

    PatternNodeTypeBuilder(root).build()

    child_pattern_type = PatternNodeTypeBuilder(child)

    assert child_pattern_type.any_ancestor_is_mnemonic() is True


def test_recursive_build():
    child = create_test_node("child")
    parent = create_test_node("$deref", children=[child])
    grandparent = create_test_node("mnemonic", children=[parent])

    parent_builder = PatternNodeParentsBuilder(grandparent)
    parent_builder.build()

    builder_type = PatternNodeTypeBuilder(grandparent)
    builder_type.build()

    type_builder = PatternNodeTypeBuilder(child)
    type_builder.build()
    builder = PatternNodeTypeBuilder(parent)
    builder.build()

    assert parent.pattern_node_type == PatternNodeTypes.deref
    assert child.pattern_node_type == PatternNodeTypes.deref_property


def test_remove_access_suffix():
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern.32") == "pattern"
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern.16") == "pattern"
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern.8l") == "pattern"
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern.8h") == "pattern"
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern") == "pattern"
    assert RegisterCaptureGroupProcessor.remove_access_suffix("pattern.other") == "pattern.other"
