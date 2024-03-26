from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_call_common import (
    CaptureGroupCallRegexBuilder,
)
from jasm.regex.tree_generators.capture_group import (
    CaptureGroupIndexInstruction,
    CaptureGroupIndexOperand,
)
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeCaptureGroupCallInstruction(PatternNode):
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
        return self.get_capture_group_call_instruction()

    def get_capture_group_call_instruction(self) -> str:
        """Capture group call"""
        capture_group_instance = CaptureGroupIndexInstruction(pattern_node=self)
        return CaptureGroupCallRegexBuilder(capture_group_instance).build()


class PatternNodeCaptureGroupReferenceInstruction(PatternNode):
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
        return self.get_capture_group_reference()

    @staticmethod
    def get_capture_group_reference() -> str:
        """Capture group reference"""
        return rf"{IGNORE_INST_ADDR}([^|]+),\|"


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
