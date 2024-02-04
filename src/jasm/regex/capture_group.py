from jasm.global_definitions import IGNORE_INST_ADDR, CaptureGroupMode
from jasm.regex.pattern_node import CAPTURE_GROUPS_REFERENCES


class CaptureGroupIndex:
    def __init__(self, str_index: str, mode: CaptureGroupMode) -> None:
        self.index = self.get_capture_group_reference(str_index)
        self.mode = mode

    @staticmethod
    def get_capture_group_reference(str_index: str) -> int:
        """The index system uses a sequence of ints and points"""
        for elem in CAPTURE_GROUPS_REFERENCES:
            if elem == str_index:
                assert isinstance(elem, str)
                return CAPTURE_GROUPS_REFERENCES.index(elem) + 1
        raise ValueError(f"Capture group reference {str_index} not found")

    def to_regex(self) -> str:
        if self.mode == CaptureGroupMode.instruction:
            return rf"{IGNORE_INST_ADDR}\{self.index},"

        if self.mode == CaptureGroupMode.operand:
            return rf"\{self.index},"
        raise ValueError(f"Capture group mode {self.mode} not found")
