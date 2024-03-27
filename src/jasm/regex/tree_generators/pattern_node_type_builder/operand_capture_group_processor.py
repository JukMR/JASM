from typing import TYPE_CHECKING

from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import (
    PatternNodeCaptureGroupOperandCall,
    PattterNodeCaptureGroupOperandReference,
)
from jasm.regex.tree_generators.shared_context import SharedContext

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

        shared_context: SharedContext = self.pattern_node.pattern_node.shared_context
        pattern_node_name = self.pattern_node.pattern_node.name

        assert isinstance(shared_context, SharedContext)
        assert isinstance(pattern_node_name, str)

        if not shared_context.is_initialized:
            return False

        return shared_context.capture_is_registered(pattern_node_name)

    def _process_operand_call(self) -> PatternNode:
        return PatternNodeCaptureGroupOperandCall(self.pattern_node.pattern_node)

    def _process_operand_reference(self) -> PatternNode:
        # Return reference
        # Add reference to the list of references
        self.add_new_references_to_global_list()
        return PattterNodeCaptureGroupOperandReference(self.pattern_node.pattern_node)

    def add_new_references_to_global_list(self) -> None:
        """Add new references to global list"""

        shared_context: SharedContext = self.pattern_node.pattern_node.shared_context
        pattern_node_name = self.pattern_node.pattern_node.name

        assert isinstance(shared_context, SharedContext)
        assert isinstance(pattern_node_name, str)

        if not shared_context.is_initialized():
            shared_context.initialize()

        if not shared_context.capture_is_registered(pattern_node_name):
            assert isinstance(pattern_node_name, str)
            shared_context.add_capture(pattern_node_name)
