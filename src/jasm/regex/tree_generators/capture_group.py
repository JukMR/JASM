from typing import List, Optional

from jasm.global_definitions import IGNORE_INST_ADDR, CaptureGroupMode


class CaptureGroupIndex:
    """Class to represent a capture group index."""

    def __init__(self, str_index: str, mode: CaptureGroupMode) -> None:
        self.index = self.get_capture_group_reference(str_index)
        self.mode = mode
        self.capture_group_references: Optional[List[str]]

    def get_capture_group_reference(self, str_index: str) -> int:
        """Get the index of the capture group reference in the list of capture group references."""
        if self.capture_group_references is None:
            raise ValueError("capture_group_references not set")

        for elem in self.capture_group_references:
            if elem == str_index:
                return self.capture_group_references.index(elem) + 1
        raise ValueError(f"Capture group reference {str_index} not found")

    def to_regex(self) -> str:
        """Return the regex representation of the capture group index."""
        match self.mode:
            case CaptureGroupMode.instruction:
                return rf"{IGNORE_INST_ADDR}\{self.index},\|"

            case CaptureGroupMode.operand:
                return rf"\{self.index},"

        raise ValueError(f"Capture group mode {self.mode} not found")
