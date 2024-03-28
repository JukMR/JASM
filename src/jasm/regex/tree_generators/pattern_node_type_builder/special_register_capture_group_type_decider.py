from typing import TYPE_CHECKING

from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterReferenceBasereg,
    PatternNodeCaptureGroupRegisterReferenceGenreg,
    PatternNodeCaptureGroupRegisterReferenceIndreg,
    PatternNodeCaptureGroupRegisterReferenceStackreg,
)

# Used this to import PatternNodeTypeBuilder type hint avoiding circular import
if TYPE_CHECKING:
    from jasm.regex.tree_generators.pattern_node_type_builder.pattern_node_type_builder import PatternNodeTypeBuilder


class SpecialRegisterCaptureGroupTypeBuilder:

    def __init__(self, pattern_node: "PatternNodeTypeBuilder") -> None:
        self.pattern_node_type_builder: PatternNodeTypeBuilder = pattern_node

        assert isinstance(pattern_node.pattern_node.name, str)
        self.pattern_name: str = pattern_node.pattern_node.name

    def process(self) -> PatternNode:
        if self.is_genreg():
            return PatternNodeCaptureGroupRegisterReferenceGenreg(self.pattern_node_type_builder.pattern_node)
        if self.is_indreg():
            return PatternNodeCaptureGroupRegisterReferenceIndreg(self.pattern_node_type_builder.pattern_node)
        if self.is_stackreg():
            return PatternNodeCaptureGroupRegisterReferenceStackreg(self.pattern_node_type_builder.pattern_node)
        if self.is_basereg():
            return PatternNodeCaptureGroupRegisterReferenceBasereg(self.pattern_node_type_builder.pattern_node)

        raise ValueError("Register type not found")

    def is_genreg(self) -> bool:
        "Check if the current node is a genreg"
        if not self.pattern_name:
            return False
        return self.pattern_name.startswith("&genreg")

    def is_indreg(self) -> bool:
        "Check if the current node is an indreg"
        if not self.pattern_name:
            return False
        return self.pattern_name.startswith("&indreg")

    def is_stackreg(self) -> bool:
        "Check if the current node is a stackreg"
        if not self.pattern_name:
            return False
        return self.pattern_name.startswith("&stackreg")

    def is_basereg(self) -> bool:
        "Check if the current node is a basereg"
        if not self.pattern_name:
            return False
        return self.pattern_name.startswith("&basereg")
