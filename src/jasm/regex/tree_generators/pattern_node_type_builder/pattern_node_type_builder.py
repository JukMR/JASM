from typing import Optional

from jasm.global_definitions import PatternNodeName
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_instruction import (
    PatternNodeCaptureGroupInstructionCall,
    PatternNodeCaptureGroupInstructionReference,
)
from jasm.regex.tree_generators.pattern_node_implementations.deref import (
    PatternNodeDeref,
    PatternNodeDerefProperty,
    PatternNodeDerefPropertyCaptureGroupCall,
    PatternNodeDerefPropertyCaptureGroupReference,
)
from jasm.regex.tree_generators.pattern_node_implementations.mnemonic_and_operand.mnemonic_and_operand import (
    PatternNodeMnemonic,
    PatternNodeOperand,
)
from jasm.regex.tree_generators.pattern_node_implementations.node_branch_root import (
    PatternNodeNode,
    PatternNodeRoot,
    PatternNodeTimes,
)
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.pattern_node_type_builder.capture_group_interface import CaptureGroupHelper
from jasm.regex.tree_generators.pattern_node_type_builder.operand_capture_group_builder import (
    OperandCaptureGroupBuilder,
)
from jasm.regex.tree_generators.pattern_node_type_builder.register_capture_group_builder import (
    RegisterCaptureGroupBuilder,
)


class PatternNodeTypeBuilder:

    def __init__(self) -> None:
        self.pattern_node: PatternNodeTmpUntyped

    def _build_current_node(self) -> PatternNode:
        return self._get_type()

    def _get_type(self) -> PatternNode:
        if getattr(self.pattern_node, "name", None) is None:
            raise ValueError("Name is not defined")

        name: PatternNodeName = self.pattern_node.name

        # Is root node
        if self.pattern_node.parent is None:
            return PatternNodeRoot(self.pattern_node)

        if isinstance(name, str):
            result = self.get_type_when_str(name)
            if result is not None:
                return result

        # Is operand
        if isinstance(name, int):
            result = self._get_type_when_int()
            if result is not None:
                return result

        if self.any_ancestor_is_mnemonic():
            return PatternNodeOperand(self.pattern_node)

        # Else is mnemonic
        return PatternNodeMnemonic(self.pattern_node)

    def get_type_when_str(self, name: str) -> Optional[PatternNode]:
        """Get the type of the node when the name is a string."""

        # CAPTURE GROUP TYPES
        # Is a capture group reference

        if name == "$deref":
            return PatternNodeDeref(self.pattern_node)

        if self.is_ancestor_deref():
            if self._is_deref_property_capture_group():

                if self._is_registry_capture_group():
                    return RegisterCaptureGroupBuilder(self.pattern_node).process()

                if self.has_any_ancestor_who_is_capture_group_reference():
                    return PatternNodeDerefPropertyCaptureGroupCall(self.pattern_node)

                self.add_new_references_to_global_list()
                return PatternNodeDerefPropertyCaptureGroupReference(self.pattern_node)
            return PatternNodeDerefProperty(self.pattern_node)

        if name.startswith("&"):
            return self._process_capture_group()

        # Is times
        if name == "times":
            return PatternNodeTimes(self.pattern_node)

        # Is node
        if self._is_node(name):
            return PatternNodeNode(self.pattern_node)

        return None

    def _process_capture_group(self) -> PatternNode:
        # Is Capture Group in operand or is a special register capture
        if self._is_capture_group_operand_or_special_register_capture():
            return self._process_capture_operand_and_register_capture()

        # Is Capture Group in Mnemonic
        return self._process_capture_group_mnemonic()

    def _is_capture_group_operand_or_special_register_capture(self) -> bool:
        "Check if the current node is a capture group operand"
        if not self.pattern_node.parent:
            return False

        if isinstance(self.pattern_node.parent, PatternNodeMnemonic):
            return True

        return False

    def _process_capture_operand_and_register_capture(self) -> PatternNode:
        if self._is_registry_capture_group():
            # Register capture group
            return RegisterCaptureGroupBuilder(self.pattern_node).process()

        # Operand capture group
        return OperandCaptureGroupBuilder(self.pattern_node).process()

    def _is_registry_capture_group(self) -> bool:
        "Check if the current node is a registry capture group"
        if not self.pattern_node.name:
            raise ValueError("Name is not defined")

        com_name = self.pattern_node.name
        assert isinstance(com_name, str)

        return (
            com_name.startswith("&genreg")
            or com_name.startswith("&indreg")
            or com_name.startswith("&stackreg")
            or com_name.startswith("&basereg")
        )

    def _process_capture_group_mnemonic(self) -> PatternNode:
        # Add this macro to refence list
        # Check it it should be a new reference or a call to an existing one
        if self.has_any_ancestor_who_is_capture_group_reference():
            # Do the call
            return PatternNodeCaptureGroupInstructionCall(self.pattern_node)

        # Create the reference
        self.add_new_references_to_global_list()
        return PatternNodeCaptureGroupInstructionReference(self.pattern_node)

    def _get_type_when_int(self) -> PatternNode:
        if self.is_ancestor_deref():
            return PatternNodeDerefProperty(self.pattern_node)

        return PatternNodeOperand(self.pattern_node)

    @staticmethod
    def _is_node(name: str) -> bool:
        if name in ["$or", "$and", "$not", "$and_any_order"]:
            return True
        return False

    def is_ancestor_deref(self) -> bool:
        "Check if the parent is a deref"
        current_node = self.pattern_node.parent
        while current_node:
            if isinstance(current_node, PatternNodeDeref):
                return True
            current_node = current_node.parent
        return False

    def any_ancestor_is_mnemonic(self) -> bool:
        "Check if any ancestor is a mnemonic"

        current_node = self.pattern_node.parent

        while current_node:
            if isinstance(current_node, PatternNodeMnemonic):
                return True
            current_node = current_node.parent
        return False

    def has_any_ancestor_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert isinstance(self.pattern_node.name, str)

        return CaptureGroupHelper().has_any_ancestor_who_is_capture_group_reference(  # type:ignore
            capture_manager=self.pattern_node.shared_context.capture_manager,
            pattern_node_name=self.pattern_node.name,
        )

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"

        assert isinstance(self.pattern_node.name, str)
        CaptureGroupHelper().add_new_references_to_global_list(
            capture_manager=self.pattern_node.shared_context.capture_manager, pattern_node_name=self.pattern_node.name
        )

    def _is_deref_property_capture_group(self) -> bool:
        "Check if the current node is a deref property capture group"
        if not self.pattern_node.parent:
            raise ValueError("Parent is not defined")

        if isinstance(self.pattern_node.name, str) and self.pattern_node.name.startswith("&"):
            return True

        return False

    def build(self, pattern_node: PatternNodeTmpUntyped, parent: Optional[PatternNode]) -> PatternNode:

        self.pattern_node = pattern_node
        self.pattern_node.parent = parent

        # Here we are just checking that the node is a PatternNode because it is useful for testing purposes to inject a
        # Typed PatternNode
        assert isinstance(pattern_node, PatternNode)

        new_concrete_instance = self._build_current_node()

        if new_concrete_instance.children:
            new_concrete_instance.children = [
                self.build(pattern_node=child, parent=new_concrete_instance) for child in new_concrete_instance.children
            ]

        return new_concrete_instance