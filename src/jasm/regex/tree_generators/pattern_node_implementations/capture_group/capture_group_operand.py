from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperandCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupOperandCall(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    def get_capture_group_call_operand(self) -> str:
        """Capture group call operand"""
        return CaptureGroupIndexOperandCall(pattern_node=self).to_regex()


class PattterNodeCaptureGroupOperandReference(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_operand()

    @staticmethod
    def get_capture_group_reference_operand() -> str:
        """Get the operand value"""
        return r"([^,|]+),"
