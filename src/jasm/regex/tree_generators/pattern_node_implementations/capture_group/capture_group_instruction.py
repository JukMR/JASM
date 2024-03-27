from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexInstructionCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupInstructionCall(PatternNode):

    def get_regex(self) -> str:
        return self.get_capture_group_call_instruction()

    def get_capture_group_call_instruction(self) -> str:
        """Capture group call"""
        return CaptureGroupIndexInstructionCall(pattern_node=self).to_regex()


class PatternNodeCaptureGroupInstructionReference(PatternNode):

    def get_regex(self) -> str:
        return self.get_capture_group_reference()

    @staticmethod
    def get_capture_group_reference() -> str:
        """Capture group reference"""
        return rf"{IGNORE_INST_ADDR}([^|]+),\|"
