from typing import List

from jasm.global_definitions import IGNORE_INST_ADDR


class CaptureGroupIndex:
    def __init__(self, str_index: str) -> None:
        self.index = self.get_capture_group_reference(str_index)

    @staticmethod
    def get_capture_group_reference(str_index: str) -> List[str]:
        """The index system uses a sequence of ints and points"""
        index = str_index.replace("$", "")
        return index.split(".")

    def to_regex(self) -> str:
        return f"{IGNORE_INST_ADDR}\\{self.index[0]}"
