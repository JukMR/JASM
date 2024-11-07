from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from enum import Enum, auto
from jasm.global_definitions import PatternNodeName
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.jasm_regex.tree_generators.pattern_node_implementations.deref import (
    PatternNodeDeref,
    PatternNodeDerefProperty,
)
from jasm.jasm_regex.tree_generators.pattern_node_implementations.mnemonic_and_operand.mnemonic_and_operand import (
    PatternNodeMnemonic,
    PatternNodeOperand,
)
from jasm.jasm_regex.tree_generators.pattern_node_type_builder.capture_group_builders import (
    OperandCaptureGroupBuilder, SpecialRegisterCaptureGroupBuilder, IntructionCaptureGroupBuilder,
    DerefCaptureGroupBuilder
)

from jasm.jasm_regex.tree_generators.pattern_node_implementations.node_branch_root import (
    PatternNodeTimes,
    NodeAnd,
    NodeNot,
    NodeOr,
    NodeAndAnyOrder,
)
from jasm.jasm_regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped


# make an enum of type of fathers; MNEMONIC- DEREF
class FatherType(Enum):
    MNEMONIC = auto()
    DEREF = auto()


@dataclass
class BuildContext:
    ancester_type: FatherType


class NodeHandler(ABC):

    def __init__(
        self,
        next_handler: Optional['NodeHandler'] = None,
    ) -> None:
        self.next_handler = next_handler

    @abstractmethod
    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:

        if self.next_handler is None:
            raise ValueError("No handler found")
        return self.next_handler.handle(node, build_context)


class NaryOperatorHandler(NodeHandler):
    wanted_name: str

    def _handle_children(
        self, node: 'PatternNodeTmpUntyped', build_context: Optional[BuildContext] = None
    ) -> None:
        if not node.children:
            raise ValueError(f"Children list is empty for {str(node.name)}")
        # get the list of children
        children = node.children
        # clear the children list
        node.children = []

        for child in children:
            builder = GeneralPatternNodeBuilder()
            node.children.append(builder.build(child, build_context))

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:

        if str(node.name) == self.wanted_name:
            self._handle_children(node, build_context)
            return self._build_node(node)
        return self.next_handler.handle(node, build_context)

    @abstractmethod
    def _build_node(self, node: PatternNodeTmpUntyped) -> PatternNode:
        pass


class AndHandler(NaryOperatorHandler):
    wanted_name = "$and"

    def _build_node(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return NodeAnd(node)


class OrHandler(NaryOperatorHandler):
    wanted_name = "$or"

    def _build_node(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return NodeOr(node)


class NotHandler(NodeHandler):
    wanted_name = "$not"

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        if str(node.name) == self.wanted_name:
            if not node.children:
                raise ValueError(f"Children list is empty for {str(node.name)}")
            if len(node.children) != 1:
                raise ValueError(f"Children list should have only one element for {str(node.name)}")
            builder = GeneralPatternNodeBuilder()
            node.children[0] = builder.build(node.children[0])
            return NodeNot(node)
        return self.next_handler.handle(node, build_context)


class AndAnyOrderHandler(NaryOperatorHandler):
    wanted_name = "$and_any_order"

    def _build_node(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return NodeAndAnyOrder(node)


class MnemonicHandler(NodeHandler):

    def _handle_children(self, node: 'PatternNodeTmpUntyped') -> None:
        if not node.children:
            return

        children = node.children
        node.children = []
        for child in children:
            node.children.append(
                OperandBuilder().build(child, BuildContext(ancester_type=FatherType.MNEMONIC))
            )

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        # this is the last handler in the chain
        self._handle_children(node)
        return PatternNodeMnemonic(node)


class DerefPropertyHandler(NodeHandler):

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:

        return PatternNodeDerefProperty(node)


class OperandHandler(NodeHandler):

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        return PatternNodeOperand(node)


class TimesHandler(NodeHandler):

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        if str(node.name) == "times":
            return PatternNodeTimes(node)
        return self.next_handler.handle(node, build_context)


class DerefHandler(NodeHandler):

    def _build_grandchildren(self, node: 'PatternNodeTmpUntyped') -> None:
        if not node.children:
            raise ValueError(f"Children list is empty for {str(node.name)}")
        children = node.children
        node.children = []

        for child in children:
            builder = DerefChildrenBuilder()
            node.children.append(builder.build(child, BuildContext(ancester_type=FatherType.DEREF)))

    def _handle_children(self, node: 'PatternNodeTmpUntyped') -> None:
        children = node.children
        node.children = []
        for child in children:
            self._build_grandchildren(child)
            node.children.append(PatternNodeDerefProperty(child))

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        if str(node.name) == "$deref":
            self._handle_children(node)
            return PatternNodeDeref(node)
        return self.next_handler.handle(node, build_context)


class CaptureGroupHandler(NodeHandler):

    def _is_capture_group(self, node_name: PatternNodeName) -> bool:
        return str(node_name).startswith("&")

    @abstractmethod
    def _construct_capture_group(self, node: PatternNodeTmpUntyped) -> PatternNode:
        pass

    def handle(
        self, node: PatternNode, build_context: Optional[BuildContext] = None
    ) -> PatternNode | None:
        if self._is_capture_group(str(node.name)):
            return self._construct_capture_group(node)
        return self.next_handler.handle(node, build_context)


class InstructionCaptureGroupHandler(CaptureGroupHandler):

    def _construct_capture_group(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return IntructionCaptureGroupBuilder().build(node)


class OperandCaptureGroupHandler(CaptureGroupHandler):

    def _construct_capture_group(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return OperandCaptureGroupBuilder().build(node)


class DerefOperandCaptureGroupHandler(CaptureGroupHandler):

    def _construct_capture_group(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return DerefCaptureGroupBuilder().build(node)


class SpecialRegisterCaptureGroupHandler(CaptureGroupHandler):

    def _is_capture_group(self, node_name: PatternNodeName) -> bool:
        # check if startswith &genreg, &indreg, &stackreg, &basereg
        start_str = [
            "&genreg",
            "&indreg",
            "&stackreg",
            "&basereg",
        ]
        for start in start_str:
            if str(node_name).startswith(start):
                return True
        return False

    def _construct_capture_group(self, node: PatternNodeTmpUntyped) -> PatternNode:
        return SpecialRegisterCaptureGroupBuilder().build(node)


class LeafHandler(NodeHandler):

    def handle(
        self, node: PatternNodeTmpUntyped, build_context: Optional[BuildContext] = None
    ) -> PatternNode:
        if build_context is None:
            return MnemonicHandler().handle(node)
        if build_context.ancester_type == FatherType.MNEMONIC:
            return OperandHandler().handle(node)
        if build_context.ancester_type == FatherType.DEREF:
            return DerefPropertyHandler().handle(node)


class NodeBuilder(ABC):

    def build(
        self, pattern_node: 'PatternNodeTmpUntyped', build_context: Optional[BuildContext] = None
    ) -> PatternNode:
        return self.build_handler_chain().handle(pattern_node, build_context)

    @abstractmethod
    def build_handler_chain(self) -> NodeHandler:
        pass


class DerefChildrenBuilder(NodeBuilder):

    def build_handler_chain(self) -> NodeHandler:
        return SpecialRegisterCaptureGroupHandler(
            DerefOperandCaptureGroupHandler(
                AndHandler(OrHandler(NotHandler(AndAnyOrderHandler(DerefPropertyHandler()))))
            )
        )


class OperandBuilder(NodeBuilder):

    def build_handler_chain(self) -> NodeHandler:
        return AndHandler(
            OrHandler(
                NotHandler(
                    AndAnyOrderHandler(
                        TimesHandler(
                            DerefHandler(
                                SpecialRegisterCaptureGroupHandler(
                                    OperandCaptureGroupHandler(OperandHandler())
                                )
                            )
                        )
                    )
                )
            )
        )


class GeneralPatternNodeBuilder(NodeBuilder):

    def build_handler_chain(self) -> NodeHandler:
        # Chain handlers together, starting with the most specific
        return AndHandler(
            OrHandler(
                NotHandler(
                    AndAnyOrderHandler(
                        DerefHandler(TimesHandler(InstructionCaptureGroupHandler(LeafHandler())))
                    )
                )
            )
        )
