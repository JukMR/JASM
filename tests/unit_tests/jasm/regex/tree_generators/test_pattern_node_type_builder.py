import pytest

from jasm.global_definitions import TimeType
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeTypes
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder


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
        ("1", PatternNodeTypes.root),
        ("$or", PatternNodeTypes.root),
    ],
)
def test_get_type(name, expected_type):
    node = create_test_node(name)
    builder = PatternNodeTypeBuilder(node)
    assert builder._get_type() == expected_type


def test_is_ancestor_deref():
    child = create_test_node("child", parent=[], children=[])
    parent = create_test_node("$deref", children=[child])
    builder = PatternNodeTypeBuilder(parent)
    builder.build()

    assert builder.command.pattern_node_type == PatternNodeTypes.deref
    assert builder.command.children
    assert builder.command.children[0]
    assert builder.command.children[0].pattern_node_type == PatternNodeTypes.mnemonic

    child2 = create_test_node("child2", parent=builder.command)
    child2_builder = PatternNodeTypeBuilder(child2)
    assert child2_builder.is_ancestor_deref() is True


def test_any_ancestor_is_mnemonic():
    child = create_test_node("child")
    parent = create_test_node("parent", children=[child])
    grandparent = create_test_node("mnemonic", children=[parent])

    parent_builder = PatternNodeParentsBuilder(grandparent)
    parent_builder.build()

    builder_type = PatternNodeTypeBuilder(grandparent)
    builder_type.build()

    type_builder = PatternNodeTypeBuilder(child)
    type_builder.build()

    assert type_builder.any_ancestor_is_mnemonic() is True


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
