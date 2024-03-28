from jasm.global_definitions import remove_access_suffix
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterCall,
)
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.pattern_node_type_builder.capture_group_interface import CaptureGroupHelper
from jasm.regex.tree_generators.pattern_node_type_builder.special_register_capture_group_type_decider import (
    SpecialRegisterCaptureGroupTypeBuilder,
)


class RegisterCaptureGroupBuilder:

    def __init__(self, pattern_node_tmp_untyped: PatternNodeTmpUntyped) -> None:
        self.pattern_node_tmp_untyped = pattern_node_tmp_untyped

    def process(self) -> PatternNode:
        return self.process_registry_capture_group()

    def process_registry_capture_group(self) -> PatternNode:
        if self.has_any_ancestor_who_is_capture_group_reference_register():
            return PatternNodeCaptureGroupRegisterCall(self.pattern_node_tmp_untyped)

        self.add_new_references_to_global_list()

        # Decide which type of register capture group it is
        return SpecialRegisterCaptureGroupTypeBuilder(pattern_node_untyped=self.pattern_node_tmp_untyped).process()

    def has_any_ancestor_who_is_capture_group_reference_register(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert isinstance(self.pattern_node_tmp_untyped.name, str)
        main_reference_name = remove_access_suffix(pattern_name=self.pattern_node_tmp_untyped.name)

        return CaptureGroupHelper().has_any_ancestor_who_is_capture_group_reference(
            shared_context=self.pattern_node_tmp_untyped.shared_context,
            pattern_node_name=main_reference_name,
        )

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"

        assert isinstance(self.pattern_node_tmp_untyped.name, str)
        pattern_node_name_without_suffix = remove_access_suffix(pattern_name=self.pattern_node_tmp_untyped.name)

        CaptureGroupHelper().add_new_references_to_global_list(
            shared_context=self.pattern_node_tmp_untyped.shared_context,
            pattern_node_name=pattern_node_name_without_suffix,
        )
