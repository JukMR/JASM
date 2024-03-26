from typing import Optional

from jasm.global_definitions import remove_access_suffix
from jasm.regex.tree_generators.pattern_node import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_instruction import (
    PatternNodeCaptureGroupCallInstruction,
    PatternNodeCaptureGroupReferenceInstruction,
)
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_operand import (
    PatternNodeCaptureGroupCallOperand,
    PattterNodeCaptureGroupReferenceOperand,
)
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_register import (
    PatternNodeCaptureGroupRegisterCall,
    PatternNodeCaptureGroupRegisterReferenceBasereg,
    PatternNodeCaptureGroupRegisterReferenceGenreg,
    PatternNodeCaptureGroupRegisterReferenceIndreg,
    PatternNodeCaptureGroupRegisterReferenceStackreg,
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
from jasm.regex.tree_generators.pattern_node_implementations.pattern_node_implementations import (
    PatternNodeNode,
    PatternNodeRoot,
    PatternNodeTimes,
)


class PatternNodeTypeBuilder:
    def __init__(self, pattern_node: PatternNode, parent: Optional[PatternNode]) -> None:

        assert isinstance(pattern_node, PatternNode)
        self.pattern_node = pattern_node
        self.pattern_node.parent = parent

    def _get_type(self) -> PatternNode:
        if getattr(self.pattern_node, "name", None) is None:
            raise ValueError("Name is not defined")

        name: str | int = self.pattern_node.name

        # Is root node
        if self.pattern_node.parent is None:
            return PatternNodeRoot(self.pattern_node)

        if isinstance(name, str):
            result = self.get_type_when_str(name)
            if result is not None:
                return result

        # Is operand
        if isinstance(name, int):
            result = self.get_type_when_int()
            if result is not None:
                return result

        if self.is_father_is_mnemonic():
            return PatternNodeOperand(self.pattern_node)

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
            if self.is_deref_property_capture_group():

                if self.is_registry_capture_group():
                    return RegisterCaptureGroupProcessor(self).process()

                if self.has_any_ancester_who_is_capture_group_reference():
                    return PatternNodeDerefPropertyCaptureGroupCall(self.pattern_node)

                self.add_new_references_to_global_list()
                return PatternNodeDerefPropertyCaptureGroupReference(self.pattern_node)
            return PatternNodeDerefProperty(self.pattern_node)

        if name.startswith("&"):
            return self.process_capture_group()

        # Is times
        if name == "times":
            return PatternNodeTimes(self.pattern_node)

        # Is node
        if self.is_node(name):
            return PatternNodeNode(self.pattern_node)

        return None

    def process_capture_group(self) -> PatternNode:
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
        if self.is_registry_capture_group():
            # Register capture group
            return RegisterCaptureGroupProcessor(self).process()

        # Operand capture group
        return OperandCaptureGroupProcessor(self).process()

    def is_registry_capture_group(self) -> bool:
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
        if self.has_any_ancester_who_is_capture_group_reference():
            # Do the call
            return PatternNodeCaptureGroupCallInstruction(self.pattern_node)

        # Create the reference
        self.add_new_references_to_global_list()
        return PatternNodeCaptureGroupReferenceInstruction(self.pattern_node)

    def get_type_when_int(self) -> PatternNode:
        if self.is_ancestor_deref():
            return PatternNodeDerefProperty(self.pattern_node)

        return PatternNodeOperand(self.pattern_node)

    @staticmethod
    def is_node(name: str) -> bool:
        if name in ["$or", "$and", "$not", "$and_any_order"]:
            return True
        return False

    def set_type(self) -> PatternNode:
        return self._get_type()

    def is_father_is_mnemonic(self) -> bool:
        "Check if the parent is a mnemonic"
        if not self.pattern_node.parent:
            return False
        return isinstance(self.pattern_node.parent, PatternNodeMnemonic)

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

    def has_any_ancester_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.pattern_node.root_node
        assert hasattr(self.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.root_node.capture_group_references is None:
            return False

        if self.pattern_node.name in self.pattern_node.root_node.capture_group_references:
            return True
        return False

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"

        assert self.pattern_node.root_node
        assert hasattr(self.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.root_node.capture_group_references is None:
            self.pattern_node.root_node.capture_group_references = []

        if self.pattern_node.name not in self.pattern_node.root_node.capture_group_references:
            assert isinstance(self.pattern_node.name, str)
            self.pattern_node.root_node.capture_group_references.append(self.pattern_node.name)

    def is_deref_property_capture_group(self) -> bool:
        "Check if the current node is a deref property capture group"
        if not self.pattern_node.parent:
            raise ValueError("Parent is not defined")

        if isinstance(self.pattern_node.name, str) and self.pattern_node.name.startswith("&"):
            return True

        return False

    def build(self) -> PatternNode:

        if self.pattern_node.parent:
            self.pattern_node.root_node = self.pattern_node.parent.root_node

        new_concrete_instance = self.set_type()

        # Add the capture group references to the root node
        if isinstance(new_concrete_instance, PatternNodeRoot):
            setattr(new_concrete_instance, "capture_group_references", [])
            new_concrete_instance.root_node = new_concrete_instance

        if new_concrete_instance.children:
            new_concrete_instance.children = [
                PatternNodeTypeBuilder(child, parent=new_concrete_instance).build()
                for child in new_concrete_instance.children
            ]

        return new_concrete_instance


class OperandCaptureGroupProcessor:

    def __init__(self, pattern_node_type_builder: PatternNodeTypeBuilder) -> None:
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

        assert self.pattern_node.pattern_node.root_node
        assert hasattr(self.pattern_node.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.pattern_node.root_node.capture_group_references is None:
            return False

        if self.pattern_node.pattern_node.name in self.pattern_node.pattern_node.root_node.capture_group_references:
            return True
        return False

    def _process_operand_call(self) -> PatternNode:
        return PatternNodeCaptureGroupCallOperand(self.pattern_node.pattern_node)

    def _process_operand_reference(self) -> PatternNode:
        # Return reference
        # Add reference to the list of references
        self.add_new_references_to_global_list()
        return PattterNodeCaptureGroupReferenceOperand(self.pattern_node.pattern_node)

    def add_new_references_to_global_list(self) -> None:
        """Add new references to global list"""

        assert self.pattern_node.pattern_node.root_node
        assert hasattr(self.pattern_node.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.pattern_node.root_node.capture_group_references is None:
            self.pattern_node.pattern_node.root_node.capture_group_references = []

        if self.pattern_node.pattern_node.name not in self.pattern_node.pattern_node.root_node.capture_group_references:
            assert isinstance(self.pattern_node.pattern_node.name, str)
            self.pattern_node.pattern_node.root_node.capture_group_references.append(
                self.pattern_node.pattern_node.name
            )


class RegisterCaptureGroupProcessor:

    def __init__(self, pattern_node: PatternNodeTypeBuilder) -> None:
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

        assert self.pattern_node.pattern_node.root_node
        pattern_node_name = self.pattern_node.pattern_node.name
        assert isinstance(pattern_node_name, str)

        main_reference_name = remove_access_suffix(pattern_node_name)

        assert hasattr(self.pattern_node.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.pattern_node.root_node.capture_group_references is None:
            return False

        if main_reference_name in self.pattern_node.pattern_node.root_node.capture_group_references:
            return True
        return False

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"
        assert self.pattern_node.pattern_node.root_node
        assert hasattr(self.pattern_node.pattern_node.root_node, "capture_group_references")

        if self.pattern_node.pattern_node.root_node.capture_group_references is None:
            self.pattern_node.pattern_node.root_node.capture_group_references = []

        assert isinstance(self.pattern_node.pattern_node.name, str)
        pattern_node_name_without_suffix = remove_access_suffix(self.pattern_node.pattern_node.name)

        if pattern_node_name_without_suffix not in self.pattern_node.pattern_node.root_node.capture_group_references:
            assert isinstance(pattern_node_name_without_suffix, str)
            self.pattern_node.pattern_node.root_node.capture_group_references.append(pattern_node_name_without_suffix)


class SpecialRegisterCaptureGroupTypeDecider:

    def __init__(self, pattern_node: PatternNodeTypeBuilder) -> None:
        self.pattern_node_type_builder: PatternNodeTypeBuilder = pattern_node

        assert isinstance(pattern_node.pattern_node.name, str)
        self.pattern_name: str = pattern_node.pattern_node.name

    def process(self) -> PatternNode:
        return self._decide_and_process_capture_group_reference_register_based_on_type()

    def _decide_and_process_capture_group_reference_register_based_on_type(self) -> PatternNode:

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
