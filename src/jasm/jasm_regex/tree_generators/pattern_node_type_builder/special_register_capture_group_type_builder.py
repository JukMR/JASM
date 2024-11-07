from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.jasm_regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupSpecialRegisterReference
)
from jasm.jasm_regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped


class SpecialRegisterCaptureGroupTypeBuilder:

    def __init__(self, pattern_node_untyped: PatternNodeTmpUntyped) -> None:
        self.pattern_node_untyped: PatternNodeTmpUntyped = pattern_node_untyped

        if not isinstance(pattern_node_untyped.name, str):
            raise TypeError("Operand name must be a string")
        self.pattern_name: str = pattern_node_untyped.name

    def process(self) -> PatternNode:
        if self.is_genreg():
            return PatternNodeCaptureGroupSpecialRegisterReference(self.pattern_node_untyped, "(.)[xhl]")
        if self.is_indreg():
            return PatternNodeCaptureGroupSpecialRegisterReference(self.pattern_node_untyped, "([sd])il?")
        if self.is_stackreg():
            return PatternNodeCaptureGroupSpecialRegisterReference(self.pattern_node_untyped, "(sp)l?")
        if self.is_basereg():
            return PatternNodeCaptureGroupSpecialRegisterReference(self.pattern_node_untyped, "(bp)l?")

        raise ValueError("Register type not found")

    def is_genreg(self) -> bool:
        "Check if the current node is a genreg"
        return self.pattern_name.startswith("&genreg")

    def is_indreg(self) -> bool:
        "Check if the current node is an indreg"
        return self.pattern_name.startswith("&indreg")

    def is_stackreg(self) -> bool:
        "Check if the current node is a stackreg"
        return self.pattern_name.startswith("&stackreg")

    def is_basereg(self) -> bool:
        "Check if the current node is a basereg"
        return self.pattern_name.startswith("&basereg")
