import pytest

from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeTypes
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder


def create_test_node(name: str, parent=None, children=None, capture_group_references=None) -> PatternNode:
    node = PatternNode(
        pattern_node_dict={},
        name=name,
        times=None,
        children=children or [],
        pattern_node_type=None,
        parent=parent,
    )
    if capture_group_references is not None:
        node.capture_group_references = capture_group_references
    return node


@pytest.mark.parametrize(
    "name, expected_type",
    [
        ("$deref", PatternNodeTypes.deref),
        ("&capture_group", PatternNodeTypes.capture_group_reference),
        ("times", PatternNodeTypes.times),
        ("1", PatternNodeTypes.operand),
        ("$or", PatternNodeTypes.node),
    ],
)
def test_get_type(name, expected_type):
    node = create_test_node(name)
    builder = PatternNodeTypeBuilder(node)
    assert builder._get_type() == expected_type


def test_is_ancestor_deref():
    parent = create_test_node("$deref")
    child = create_test_node("child", parent=parent)
    builder = PatternNodeTypeBuilder(child)
    assert builder.is_ancestor_deref() is True


def test_any_ancestor_is_mnemonic():
    grandparent = create_test_node("mnemonic", capture_group_references=[])
    parent = create_test_node("parent", parent=grandparent)
    child = create_test_node("child", parent=parent)
    builder = PatternNodeTypeBuilder(child)
    assert builder.any_ancestor_is_mnemonic() is True


def test_recursive_build():
    child = create_test_node("child")
    parent = create_test_node("$deref", children=[child])
    builder = PatternNodeTypeBuilder(parent)
    builder.build()
    assert parent.pattern_node_type == PatternNodeTypes.deref
    assert child.pattern_node_type == PatternNodeTypes.deref_property
