from typing import TYPE_CHECKING

from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import (
    PatternNodeCaptureGroupOperandCall,
    PattterNodeCaptureGroupOperandReference,
)

# Used this to import PatternNodeTypeBuilder type hint avoiding circular import
if TYPE_CHECKING:
    from jasm.regex.tree_generators.pattern_node_type_builder.pattern_node_type_builder import PatternNodeTypeBuilder


class OperandCaptureGroupProcessor:

    def __init__(self, pattern_node_type_builder: "PatternNodeTypeBuilder") -> None:
        self.pattern_node = pattern_node_type_builder

    def process(self) -> PatternNode:
        return self._process_capture_group_operand()

    def _process_capture_group_operand(self) -> PatternNode:
        # Has this capture group been referenced before?
        if self.has_any_ancester_who_is_capture_group_reference():
            return self._process_operand_call()

        return self._process_operand_reference()

    def has_any_ancester_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.pattern_node.pattern_node.shared_context
        assert hasattr(self.pattern_node.pattern_node.shared_context, "capture_group_references")

        if self.pattern_node.pattern_node.shared_context.capture_group_references is None:
            return False

        if (
            self.pattern_node.pattern_node.name
            in self.pattern_node.pattern_node.shared_context.capture_group_references
        ):
            return True
        return False

    def _process_operand_call(self) -> PatternNode:
        return PatternNodeCaptureGroupOperandCall(self.pattern_node.pattern_node)

    def _process_operand_reference(self) -> PatternNode:
        # Return reference
        # Add reference to the list of references
        self.add_new_references_to_global_list()
        return PattterNodeCaptureGroupOperandReference(self.pattern_node.pattern_node)

    def add_new_references_to_global_list(self) -> None:
        """Add new references to global list"""

        assert self.pattern_node.pattern_node.shared_context
        assert hasattr(self.pattern_node.pattern_node.shared_context, "capture_group_references")

        if self.pattern_node.pattern_node.shared_context.capture_group_references is None:
            self.pattern_node.pattern_node.shared_context.capture_group_references = []

        if (
            self.pattern_node.pattern_node.name
            not in self.pattern_node.pattern_node.shared_context.capture_group_references
        ):
            assert isinstance(self.pattern_node.pattern_node.name, str)
            self.pattern_node.pattern_node.shared_context.capture_group_references.append(
                self.pattern_node.pattern_node.name
            )
