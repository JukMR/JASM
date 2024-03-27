from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_call_common import (
    CaptureGroupCallRegexBuilder,
)
from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexInstruction
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupCallInstruction(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
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
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference()

    @staticmethod
    def get_capture_group_reference() -> str:
        """Capture group reference"""
        return rf"{IGNORE_INST_ADDR}([^|]+),\|"
