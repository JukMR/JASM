from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_call_common import (
    CaptureGroupCallRegexBuilder,
)
from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperand
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeCaptureGroupCallOperand(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    def get_capture_group_call_operand(self) -> str:
        """Capture group call operand"""
        capture_group_instance = CaptureGroupIndexOperand(pattern_node=self)
        return CaptureGroupCallRegexBuilder(capture_group_instance).build()


class PattterNodeCaptureGroupReferenceOperand(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_operand()

    @staticmethod
    def get_capture_group_reference_operand() -> str:
        """Get the operand value"""
        return r"([^,|]+),"
