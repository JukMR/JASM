from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.pattern_node import CAPTURE_GROUPS_REFERENCES


class CaptureGroupIndex:
    def __init__(self, str_index: str) -> None:
        self.index = self.get_capture_group_reference(str_index)

    @staticmethod
    def get_capture_group_reference(str_index: str) -> int:
        """The index system uses a sequence of ints and points"""
        for elem in CAPTURE_GROUPS_REFERENCES:
            if elem.name == str_index:
                assert isinstance(elem.name, str)
                return CAPTURE_GROUPS_REFERENCES.index(elem) + 1
        raise ValueError(f"Capture group reference {str_index} not found")

    def to_regex(self) -> str:
        return f"{IGNORE_INST_ADDR}\\{self.index}"
