from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperandCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupOperandCall(PatternNode):

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    def get_capture_group_call_operand(self) -> str:
        """Capture group call operand"""
        return CaptureGroupIndexOperandCall(pattern_node=self).to_regex()


class PattterNodeCaptureGroupOperandReference(PatternNode):

    def get_regex(self) -> str:
        return self.get_capture_group_reference_operand()

    @staticmethod
    def get_capture_group_reference_operand() -> str:
        """Get the operand value"""
        return r"([^,|]+),"
