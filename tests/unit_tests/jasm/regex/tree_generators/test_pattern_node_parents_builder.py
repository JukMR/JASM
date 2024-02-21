from typing import List

from jasm.regex.tree_generators.pattern_node import PatternNode
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder


def create_pattern_node(name: str, children: List = None) -> PatternNode:
    return PatternNode(
        pattern_node_dict={},
        name=name,
        times=None,
        children=children,
        pattern_node_type=None,
        parent=None,
    )


def test_set_parent_with_nested_children():
    parent = create_pattern_node("parent")
    child1 = create_pattern_node("child1")
    child2 = create_pattern_node(
        "child2", children=[create_pattern_node("grandchild1"), create_pattern_node("grandchild2")]
    )

    builder = PatternNodeParentsBuilder(parent)
    builder.set_parent(parent, [child1, child2])

    # Check direct children parent assignment
    assert child1.parent is parent
    assert child2.parent is parent

    # Check nested children parent assignment
    for grandchild in child2.children:
        assert grandchild.parent is child2


def test_build_sets_parents_correctly():
    parent = create_pattern_node("parent")
    child1 = create_pattern_node("child1")
    child2 = create_pattern_node("child2")
    parent.children = [child1, child2]  # Simulate children

    builder = PatternNodeParentsBuilder(parent)
    builder.build()  # This should set parent for child1 and child2

    assert child1.parent is parent
    assert child2.parent is parent


def test_set_parent_with_no_children():
    parent = create_pattern_node("parent")
    builder = PatternNodeParentsBuilder(parent)

    # This should not raise any error
    builder.set_parent(parent, [])
