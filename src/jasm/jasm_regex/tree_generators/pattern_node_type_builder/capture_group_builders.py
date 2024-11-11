from jasm.global_definitions import remove_access_suffix
from jasm.jasm_regex.tree_generators.capture_manager import CapturesManager
from jasm.jasm_regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped

from jasm.jasm_regex.tree_generators.pattern_node_type_builder.capture_group_interface import CaptureGroupBaseBuilder
from jasm.jasm_regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import (
    PatternNodeCaptureGroupOperandCall,
    PatternNodeCaptureGroupOperandReference,
)
from jasm.jasm_regex.tree_generators.pattern_node_implementations.capture_group.capture_group_instruction import (
    PatternNodeCaptureGroupInstructionCall,
    PatternNodeCaptureGroupInstructionReference,
)
from jasm.jasm_regex.tree_generators.pattern_node_implementations.deref import (
    PatternNodeDerefPropertyCaptureGroupCall,
    PatternNodeDerefPropertyCaptureGroupReference,
)
from jasm.jasm_regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterCall,
)
from jasm.jasm_regex.tree_generators.pattern_node_type_builder.special_register_capture_group_type_builder import (
    SpecialRegisterCaptureGroupTypeBuilder,
)


class IntructionCaptureGroupBuilder(CaptureGroupBaseBuilder):

    def _process_call(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupInstructionCall:
        return PatternNodeCaptureGroupInstructionCall(untyped_node)

    def _process_register(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupInstructionReference:
        return PatternNodeCaptureGroupInstructionReference(untyped_node)


class OperandCaptureGroupBuilder(CaptureGroupBaseBuilder):

    def _process_call(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupOperandCall:
        return PatternNodeCaptureGroupOperandCall(untyped_node)

    def _process_register(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupOperandReference:
        return PatternNodeCaptureGroupOperandReference(untyped_node)


class SpecialRegisterCaptureGroupBuilder(CaptureGroupBaseBuilder):

    def _capture_is_registered(
        self, capture_manager: CapturesManager, pattern_node_name: str
    ) -> bool:
        clean_name = remove_access_suffix(pattern_name=pattern_node_name)
        return super()._capture_is_registered(capture_manager, clean_name)

    def add_new_references_to_global_list(
        self, capture_manager: CapturesManager, pattern_node_name: str
    ) -> None:
        clean_name = remove_access_suffix(pattern_name=pattern_node_name)
        super().add_new_references_to_global_list(capture_manager, clean_name)

    def _process_call(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupRegisterCall:
        return PatternNodeCaptureGroupRegisterCall(untyped_node)

    def _process_register(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeCaptureGroupRegisterCall:
        return SpecialRegisterCaptureGroupTypeBuilder(untyped_node).process()


class DerefCaptureGroupBuilder(CaptureGroupBaseBuilder):

    def _process_call(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeDerefPropertyCaptureGroupCall:
        return PatternNodeDerefPropertyCaptureGroupCall(untyped_node)

    def _process_register(
        self, untyped_node: PatternNodeTmpUntyped
    ) -> PatternNodeDerefPropertyCaptureGroupReference:
        return PatternNodeDerefPropertyCaptureGroupReference(untyped_node)
