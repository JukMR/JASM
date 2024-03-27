from typing import TYPE_CHECKING

from jasm.global_definitions import remove_access_suffix
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterCall,
)
from jasm.regex.tree_generators.pattern_node_type_builder.special_register_capture_group_type_decider import (
    SpecialRegisterCaptureGroupTypeDecider,
)

# Used this to import PatternNodeTypeBuilder type hint avoiding circular import
if TYPE_CHECKING:
    from jasm.regex.tree_generators.pattern_node_type_builder.pattern_node_type_builder import PatternNodeTypeBuilder


class RegisterCaptureGroupProcessor:

    def __init__(self, pattern_node: "PatternNodeTypeBuilder") -> None:
        self.pattern_node = pattern_node

    def process(self) -> PatternNode:
        return self.process_registry_capture_group()

    def process_registry_capture_group(self) -> PatternNode:
        if self.has_any_ancester_who_is_capture_group_reference_register():
            return PatternNodeCaptureGroupRegisterCall(self.pattern_node.pattern_node)

        self.add_new_references_to_global_list()

        # Decide which type of register capture group it is
        return SpecialRegisterCaptureGroupTypeDecider(pattern_node=self.pattern_node).process()

    def has_any_ancester_who_is_capture_group_reference_register(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.pattern_node.pattern_node.shared_context
        pattern_node_name = self.pattern_node.pattern_node.name
        assert isinstance(pattern_node_name, str)

        main_reference_name = remove_access_suffix(pattern_node_name)

        assert hasattr(self.pattern_node.pattern_node.shared_context, "capture_group_references")

        if self.pattern_node.pattern_node.shared_context.capture_group_references is None:
            return False

        if main_reference_name in self.pattern_node.pattern_node.shared_context.capture_group_references:
            return True
        return False

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"
        assert self.pattern_node.pattern_node.shared_context
        assert hasattr(self.pattern_node.pattern_node.shared_context, "capture_group_references")

        if self.pattern_node.pattern_node.shared_context.capture_group_references is None:
            self.pattern_node.pattern_node.shared_context.capture_group_references = []

        assert isinstance(self.pattern_node.pattern_node.name, str)
        pattern_node_name_without_suffix = remove_access_suffix(self.pattern_node.pattern_node.name)

        if (
            pattern_node_name_without_suffix
            not in self.pattern_node.pattern_node.shared_context.capture_group_references
        ):
            assert isinstance(pattern_node_name_without_suffix, str)
            self.pattern_node.pattern_node.shared_context.capture_group_references.append(
                pattern_node_name_without_suffix
            )
