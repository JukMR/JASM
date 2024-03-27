from abc import ABC, abstractmethod
from typing import List

from jasm.global_definitions import IGNORE_INST_ADDR, remove_access_suffix
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class CaptureGroupIndex(ABC):
    """Class to represent a capture group index."""

    def __init__(self, pattern_node: PatternNode, str_index: str) -> None:

        assert (
            hasattr(pattern_node.shared_context, "capture_group_references")
            and pattern_node.shared_context.capture_group_references is not None
        )

        self.index = pattern_node.shared_context.get_capture_index(str_index)

    @abstractmethod
    def to_regex(self) -> str:
        """Return the regex representation of the capture group index."""


class CaptureGroupIndexInstruction(CaptureGroupIndex):
    """Class to represent a capture group index for an instruction."""

    def __init__(self, pattern_node: PatternNode) -> None:
        str_index = str(pattern_node.name)
        super().__init__(pattern_node=pattern_node, str_index=str_index)

    def to_regex(self) -> str:
        return rf"{IGNORE_INST_ADDR}\{self.index},\|"


class CaptureGroupIndexOperand(CaptureGroupIndex):
    """Class to represent a capture group index for an operand."""

    def __init__(self, pattern_node: PatternNode) -> None:
        str_index = str(pattern_node.name)
        super().__init__(pattern_node=pattern_node, str_index=str_index)

    def to_regex(self) -> str:
        return rf"\{self.index}"


class CaptureGroupIndexRegister(CaptureGroupIndex):
    """Class to represent a capture group index for a register."""

    def __init__(self, pattern_node: PatternNode) -> None:
        str_index = remove_access_suffix(str(pattern_node.name))
        super().__init__(pattern_node=pattern_node, str_index=str_index)

    def to_regex(self) -> str:
        return rf"\{self.index}"
