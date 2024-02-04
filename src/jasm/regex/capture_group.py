from typing import List
from jasm.global_definitions import IGNORE_INST_ADDR, CaptureGroupMode


class CaptureGroupIndex:
    def __init__(self, str_index: str, mode: CaptureGroupMode, capture_groups_references: List[str]) -> None:
        self.capture_group_references = capture_groups_references
        self.index = self.get_capture_group_reference(str_index)
        self.mode = mode

    def get_capture_group_reference(self, str_index: str) -> int:
        for elem in self.capture_group_references:
            if elem == str_index:
                assert isinstance(elem, str)
                return self.capture_group_references.index(elem) + 1
        raise ValueError(f"Capture group reference {str_index} not found")

    def to_regex(self) -> str:
        if self.mode == CaptureGroupMode.instruction:
            return rf"{IGNORE_INST_ADDR}\{self.index},\|"

        if self.mode == CaptureGroupMode.operand:
            return rf"\{self.index},"
        raise ValueError(f"Capture group mode {self.mode} not found")
