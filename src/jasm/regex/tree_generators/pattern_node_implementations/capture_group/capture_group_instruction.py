from jasm.global_definitions import IGNORE_INST_ADDR
from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexInstructionCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupInstructionCall(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        result: str = CaptureGroupIndexInstructionCall(pattern_node=self).to_regex()
        return result


class PatternNodeCaptureGroupInstructionReference(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return rf"{IGNORE_INST_ADDR}([^|]+),\|"
