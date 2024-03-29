from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperandCall
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeCaptureGroupOperandCall(PatternNode):

    def get_regex(self) -> str:
        result: str = CaptureGroupIndexOperandCall(pattern_node=self).to_regex()
        return result


class PatternNodeCaptureGroupOperandReference(PatternNode):

    def get_regex(self) -> str:
        return r"([^,|]+),"
