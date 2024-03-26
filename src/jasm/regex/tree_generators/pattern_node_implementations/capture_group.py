from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.capture_group import CaptureGroupIndexInstruction, CaptureGroupIndexOperand
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeCaptureGroupCall(PatternNode):
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

        index = capture_group_instance.to_regex()

        return f"{index}"


class PatternNodeCaptureGroupReference(PatternNode):
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

    # Capture group call
    def get_capture_group_call_operand(self) -> str:

        capture_group_instance = CaptureGroupIndexOperand(pattern_node=self)

        index = capture_group_instance.to_regex()

        return f"{index}"


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
