from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperandCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupOperandCall(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return CaptureGroupIndexOperandCall(pattern_node=self).to_regex()  # type:ignore


class PatternNodeCaptureGroupOperandReference(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return r"([^,|]+),"
