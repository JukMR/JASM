from typing import Optional

import pytest

from jasm.global_definitions import TimesType, remove_access_suffix
from jasm.jasm_regex.tree_generators.capture_manager import CapturesManager
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode, PatternNodeData
from jasm.jasm_regex.tree_generators.pattern_node_implementations.deref import PatternNodeDeref, PatternNodeDerefProperty
from jasm.jasm_regex.tree_generators.pattern_node_implementations.mnemonic_and_operand.mnemonic_and_operand import (
    PatternNodeMnemonic, PatternNodeOperand
)
from jasm.jasm_regex.tree_generators.pattern_node_implementations.node_branch_root import NodeAnd, NodeOr
from jasm.jasm_regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.jasm_regex.tree_generators.pattern_node_type_builder.ast_builder import GeneralPatternNodeBuilder
from jasm.jasm_regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import PatternNodeCaptureGroupOperandReference, PatternNodeCaptureGroupOperandCall
from jasm.jasm_regex.tree_generators.shared_context import SharedContext


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


def test_empty_branch() -> None:

    root_node = pattern_node_base_creator(name="$and")

    # expect error due to check that branch builders should have children
    with pytest.raises(ValueError):
        root_node = GeneralPatternNodeBuilder().build(root_node)


def test_building_root_node() -> None:

    operand = pattern_node_base_creator(name="label")
    child1 = pattern_node_base_creator(name="jmp", children=[operand])

    child2 = pattern_node_base_creator(name="cmp")

    root_node = pattern_node_base_creator(name="$and", children=[child1, child2])

    root_node = GeneralPatternNodeBuilder().build(root_node)
    assert isinstance(root_node, NodeAnd)
    assert isinstance(root_node.children[0], PatternNodeMnemonic)
    assert isinstance(root_node.children[0].children[0], PatternNodeOperand)
    assert isinstance(root_node.children[1], PatternNodeMnemonic)


def test_building_capture_group() -> None:

    operand = pattern_node_base_creator(name="label")
    child1 = pattern_node_base_creator(name="jmp", children=[operand])

    childchild2 = pattern_node_base_creator(name="&cc-2")
    child2 = pattern_node_base_creator(name="call", children=[childchild2])

    childchild3 = pattern_node_base_creator(name="&cc-2")
    child3 = pattern_node_base_creator(name="call", children=[childchild3])

    root_node = pattern_node_base_creator(name="$and", children=[child1, child2, child3])

    root_node = GeneralPatternNodeBuilder().build(root_node)
    assert isinstance(root_node, NodeAnd)
    assert isinstance(root_node.children[0], PatternNodeMnemonic)
    assert isinstance(root_node.children[0].children[0], PatternNodeOperand)
    assert isinstance(root_node.children[1], PatternNodeMnemonic)
    assert isinstance(root_node.children[1].children[0], PatternNodeCaptureGroupOperandReference)
    assert isinstance(root_node.children[2], PatternNodeMnemonic)
    assert isinstance(root_node.children[2].children[0], PatternNodeCaptureGroupOperandCall)


def test_deref() -> None:
    raxnode = pattern_node_base_creator(name="rax")
    operand = pattern_node_base_creator(name="main_reg", children=[raxnode])
    nodederef = pattern_node_base_creator(name="$deref", children=[operand])
    nodeand = pattern_node_base_creator(name="$and", children=[nodederef])

    root_node = GeneralPatternNodeBuilder().build(nodeand)
    assert isinstance(root_node, NodeAnd)
    assert isinstance(root_node.children[0], PatternNodeDeref)
    assert isinstance(root_node.children[0].children[0], PatternNodeDerefProperty)
    assert isinstance(root_node.children[0].children[0].children[0], PatternNodeDerefProperty)


def test_is_ancestor_deref() -> None:
    grand_child = pattern_node_base_creator(name="grand_child")
    child = pattern_node_base_creator(name="child", children=[grand_child])
    parent = pattern_node_base_creator(name="$deref", children=[child])
    root_node = pattern_node_base_creator(name="$and", children=[parent])

    root_node = GeneralPatternNodeBuilder().build(root_node)

    parent = root_node.children[0]
    child = parent.children[0]
    assert isinstance(root_node, NodeAnd)
    assert isinstance(parent, PatternNodeDeref)
    assert parent.children
    assert child
    assert isinstance(child, PatternNodeDerefProperty)


def test_any_ancestor_is_mnemonic(mock_shared_context: SharedContext) -> None:
    parent = pattern_node_base_creator(name="operand", children=[])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    pattern_node_tree_builder = GeneralPatternNodeBuilder()
    root = pattern_node_tree_builder.build(pattern_node=root)
    assert isinstance(root, NodeAnd)
    assert isinstance(root.children[0], PatternNodeMnemonic)
    assert isinstance(root.children[0].children[0], PatternNodeOperand)


def test_nested_branches() -> None:
    op2 = pattern_node_base_creator(name="operand2")
    op1 = pattern_node_base_creator(name="operand")
    nodeor = pattern_node_base_creator(name="$or", children=[op2, op1])
    op3 = pattern_node_base_creator(name="operand3")

    node1 = pattern_node_base_creator(name="mnemonic", children=[nodeor, op3])
    root = pattern_node_base_creator(name="$and", children=[node1])

    pattern_node_tree_builder = GeneralPatternNodeBuilder()
    root = pattern_node_tree_builder.build(pattern_node=root)

    assert isinstance(root, NodeAnd)
    assert isinstance(root.children[0], PatternNodeMnemonic)
    assert isinstance(root.children[0].children[0], NodeOr)
    assert isinstance(root.children[0].children[0].children[0], PatternNodeOperand)
    assert isinstance(root.children[0].children[0].children[1], PatternNodeOperand)
    assert isinstance(root.children[0].children[1], PatternNodeOperand)



def test_recursive_build() -> None:
    granchildreg = pattern_node_base_creator(name="granchildreg")
    child = pattern_node_base_creator(name="child", children=[granchildreg])
    parent = pattern_node_base_creator(name="$deref", children=[child])
    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    root = GeneralPatternNodeBuilder().build(pattern_node=root)
    grandparent = root.children[0]
    parent = grandparent.children[0]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert isinstance(child, PatternNodeDerefProperty)


def test_recursive_build2() -> None:
    granchildreg = pattern_node_base_creator(name="granchildreg")
    child = pattern_node_base_creator(name="child", children=[granchildreg])
    parent = pattern_node_base_creator(name="$deref", children=[child])

    parent2 = pattern_node_base_creator(name="rax", children=None)

    grandparent = pattern_node_base_creator(name="mnemonic", children=[parent, parent2])
    root = pattern_node_base_creator(name="$and", children=[grandparent])

    root = GeneralPatternNodeBuilder().build(pattern_node=root)
    grandparent = root.children[0]
    parent = grandparent.children[0]
    parent2 = grandparent.children[1]
    child = parent.children[0]

    assert isinstance(parent, PatternNodeDeref)
    assert isinstance(child, PatternNodeDerefProperty)
    assert isinstance(parent2, PatternNodeOperand)


def test_remove_access_suffix() -> None:
    assert remove_access_suffix("pattern.32") == "pattern"
    assert remove_access_suffix("pattern.16") == "pattern"
    assert remove_access_suffix("pattern.8l") == "pattern"
    assert remove_access_suffix("pattern.8h") == "pattern"
    assert remove_access_suffix("pattern") == "pattern"
    assert remove_access_suffix("pattern.other") == "pattern.other"
