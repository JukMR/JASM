from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import (
    PatternNodeCaptureGroupOperandCall,
    PatternNodeCaptureGroupOperandReference,
)
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.pattern_node_type_builder.capture_group_interface import CaptureGroupHelper


class OperandCaptureGroupBuilder:

    def __init__(self, pattern_node_tmp_untyped: PatternNodeTmpUntyped) -> None:
        self.pattern_node = pattern_node_tmp_untyped

    def process(self) -> PatternNode:
        return self._process_capture_group_operand()

    def _process_capture_group_operand(self) -> PatternNode:
        # Has this capture group been referenced before?
        if self.has_any_ancestor_who_is_capture_group_reference():
            return self._process_operand_call()

        return self._process_operand_reference()

    def has_any_ancestor_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert isinstance(self.pattern_node.name, str)

        result: bool = CaptureGroupHelper().has_any_ancestor_who_is_capture_group_reference(
            capture_manager=self.pattern_node.shared_context.capture_manager,
            pattern_node_name=self.pattern_node.name,
        )
        return result

    def _process_operand_call(self) -> PatternNode:
        return PatternNodeCaptureGroupOperandCall(self.pattern_node)

    def _process_operand_reference(self) -> PatternNode:
        # Return reference
        # Add reference to the list of references
        self.add_new_references_to_global_list()
        return PatternNodeCaptureGroupOperandReference(self.pattern_node)

    def add_new_references_to_global_list(self) -> None:
        """Add new references to global list"""

        assert isinstance(self.pattern_node.name, str)
        CaptureGroupHelper().add_new_references_to_global_list(
            capture_manager=self.pattern_node.shared_context.capture_manager,
            pattern_node_name=self.pattern_node.name,
        )
