from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndex


class CaptureGroupCallRegexBuilder:
    """
    Capture group call regex builder
    This builder is used to build the regex for a capture group call

    Currently used by:
    - deref.py: PatternNodeDerefPropertyCaptureGroupCall
    - capture_group_instruction.py: PatternNodeCaptureGroupCallInstruction
    - capture_group_operand.py: PatternNodeCaptureGroupCallOperand
    """

    def __init__(self, capture_group_instance: CaptureGroupIndex) -> None:
        self.capture_group_instance = capture_group_instance

    def build(self) -> str:
        index = self.capture_group_instance.to_regex()
        return f"{index}"
