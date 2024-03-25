from typing import List

from jasm.global_definitions import IGNORE_INST_ADDR, CaptureGroupMode, remove_access_suffix
from jasm.regex.tree_generators.pattern_node import PatternNode


class CaptureGroupIndex:
    """Class to represent a capture group index."""

    # TODO: modify this class to use SubClasses instead of the mode attribute
    # Do this in the branch `feature/refactor-pattern-node-class`

    def __init__(self, pattern_node: PatternNode, mode: CaptureGroupMode) -> None:

        if mode == CaptureGroupMode.register:
            str_index = remove_access_suffix(str(pattern_node.name))
        else:
            str_index = str(pattern_node.name)

        assert (
            hasattr(pattern_node.root_node, "capture_group_references")
            and pattern_node.root_node.capture_group_references is not None
        )

        capture_group_references = pattern_node.root_node.capture_group_references
        self.index = self._get_capture_group_reference(str_index, capture_group_references)
        self.mode = mode

    @staticmethod
    def _get_capture_group_reference(str_index: str, capture_group_references: List[str]) -> int:
        """Get the index of the capture group reference in the list of capture group references."""
        for elem in capture_group_references:
            if elem == str_index:
                return capture_group_references.index(elem) + 1
        raise ValueError(f"Capture group reference {str_index} not found")

    def to_regex(self) -> str:
        """Return the regex representation of the capture group index."""
        match self.mode:
            case CaptureGroupMode.instruction:
                return rf"{IGNORE_INST_ADDR}\{self.index},\|"

            case CaptureGroupMode.operand | CaptureGroupMode.register:
                return rf"\{self.index}"

        raise ValueError(f"Capture group mode {self.mode} not found")
