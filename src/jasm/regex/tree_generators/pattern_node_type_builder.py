from typing import Optional

from jasm.global_definitions import PatternNodeTypes, RegisterCaptureSuffixs
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeTypeBuilder:
    def __init__(self, pattern_node: PatternNode) -> None:
        assert isinstance(pattern_node, PatternNode)
        self.command = pattern_node

    def _get_type(self) -> PatternNodeTypes:
        if getattr(self.command, "name", None) is None:
            raise ValueError("Name is not defined")

        name: str | int = self.command.name

        # Is root node
        if self.command.parent is None:
            return PatternNodeTypes.root

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
            return PatternNodeTypes.operand

        if self.any_ancestor_is_mnemonic():
            return PatternNodeTypes.operand

        # Else is mnemonic
        return PatternNodeTypes.mnemonic

    def get_type_when_str(self, name: str) -> Optional[PatternNodeTypes]:
        """Get the type of the node when the name is a string."""

        # CAPTURE GROUP TYPES
        # Is a capture group reference

        if name == "$deref":
            return PatternNodeTypes.deref

        if self.is_ancestor_deref():
            if self.is_deref_property_capture_group():

                if self.is_registry_capture_group():
                    return RegisterCaptureGroupProcessor(self).process()

                if self.has_any_ancester_who_is_capture_group_reference():
                    return PatternNodeTypes.deref_property_capture_group_call

                self.add_new_references_to_global_list()
                return PatternNodeTypes.deref_property_capture_group_reference
            return PatternNodeTypes.deref_property

        if name.startswith("&"):
            return self.process_capture_group()

        # Is times
        if name == "times":
            return PatternNodeTypes.times

        # Is node
        if self.is_node(name):
            return PatternNodeTypes.node

        return None

    def process_capture_group(self) -> PatternNodeTypes:
        # Is Capture Group in operand or is a special register capture
        if self._is_capture_group_operand_or_special_register_capture():
            return self._process_capture_operand_and_register_capture()

        # Is Capture Group in Mnemonic
        return self._process_capture_group_mnemonic()

    def _is_capture_group_operand_or_special_register_capture(self) -> bool:
        "Check if the current node is a capture group operand"
        if not self.command.parent:
            return False

        if self.command.parent.pattern_node_type == PatternNodeTypes.mnemonic:
            return True

        return False

    def _process_capture_operand_and_register_capture(self) -> PatternNodeTypes:
        if self.is_registry_capture_group():
            # Register capture group
            return RegisterCaptureGroupProcessor(self).process()

        # Operand capture group
        return OperandCaptureGroupProcessor(self).process()

    def is_registry_capture_group(self) -> bool:
        "Check if the current node is a registry capture group"
        if not self.command.name:
            raise ValueError("Name is not defined")

        com_name = self.command.name
        assert isinstance(com_name, str)

        return (
            com_name.startswith("&genreg")
            or com_name.startswith("&indreg")
            or com_name.startswith("&stackreg")
            or com_name.startswith("&basereg")
        )

    def _process_capture_group_mnemonic(self) -> PatternNodeTypes:
        # Add this macro to refence list
        # Check it it should be a new reference or a call to an existing one
        if self.has_any_ancester_who_is_capture_group_reference():
            # Do the call
            return PatternNodeTypes.capture_group_call

        # Create the reference
        self.add_new_references_to_global_list()
        return PatternNodeTypes.capture_group_reference

    def get_type_when_int(self) -> PatternNodeTypes:
        if self.is_ancestor_deref():
            return PatternNodeTypes.deref_property

        return PatternNodeTypes.operand

    @staticmethod
    def is_node(name: str) -> bool:
        if name in ["$or", "$and", "$not", "$and_any_order"]:
            return True
        return False

    def set_type(self) -> PatternNode:
        self.command.pattern_node_type = self._get_type()
        return self.command

    def is_father_is_mnemonic(self) -> bool:
        "Check if the parent is a mnemonic"
        if not self.command.parent:
            return False
        return self.command.parent.pattern_node_type == PatternNodeTypes.mnemonic

    def is_ancestor_deref(self) -> bool:
        "Check if the parent is a deref"
        current_node = self.command.parent
        while current_node:
            if current_node.pattern_node_type == PatternNodeTypes.deref:
                return True
            current_node = current_node.parent
        return False

    def any_ancestor_is_mnemonic(self) -> bool:
        "Check if any ancestor is a mnemonic"

        current_node = self.command.parent

        while current_node:
            if current_node.pattern_node_type == PatternNodeTypes.mnemonic:
                return True
            current_node = current_node.parent
        return False

    def has_any_ancester_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.command.root_node
        assert hasattr(self.command.root_node, "capture_group_references")

        if self.command.root_node.capture_group_references is None:
            return False

        if self.command.name in self.command.root_node.capture_group_references:
            return True
        return False

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"

        assert self.command.root_node
        assert hasattr(self.command.root_node, "capture_group_references")

        if self.command.root_node.capture_group_references is None:
            self.command.root_node.capture_group_references = []

        if self.command.name not in self.command.root_node.capture_group_references:
            assert isinstance(self.command.name, str)
            self.command.root_node.capture_group_references.append(self.command.name)

    def is_deref_property_capture_group(self) -> bool:
        "Check if the current node is a deref property capture group"
        if not self.command.parent:
            raise ValueError("Parent is not defined")

        if isinstance(self.command.name, str) and self.command.name.startswith("&"):
            return True

        return False

    def build(self) -> None:
        self.set_type()

        # Add the capture group references to the root node
        if self.command.pattern_node_type == PatternNodeTypes.root:
            setattr(self.command, "capture_group_references", [])

        if self.command.children:
            for child in self.command.children:
                PatternNodeTypeBuilder(child).build()


class OperandCaptureGroupProcessor:

    def __init__(self, pattern_node_type_builder: PatternNodeTypeBuilder) -> None:
        self.pattern_node = pattern_node_type_builder

    def process(self) -> PatternNodeTypes:
        return self._process_capture_group_operand()

    def _process_capture_group_operand(self) -> PatternNodeTypes:
        # Has this capture group been referenced before?
        if self.has_any_ancester_who_is_capture_group_reference():
            return self._process_operand_call()

        return self._process_operand_reference()

    def has_any_ancester_who_is_capture_group_reference(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.pattern_node.command.root_node
        assert hasattr(self.pattern_node.command.root_node, "capture_group_references")

        if self.pattern_node.command.root_node.capture_group_references is None:
            return False

        if self.pattern_node.command.name in self.pattern_node.command.root_node.capture_group_references:
            return True
        return False

    def _process_operand_call(self) -> PatternNodeTypes:
        return PatternNodeTypes.capture_group_call_operand

    def _process_operand_reference(self) -> PatternNodeTypes:
        # Return reference
        # Add reference to the list of references
        self.add_new_references_to_global_list()
        return PatternNodeTypes.capture_group_reference_operand

    def add_new_references_to_global_list(self) -> None:
        """Add new references to global list"""

        assert self.pattern_node.command.root_node
        assert hasattr(self.pattern_node.command.root_node, "capture_group_references")

        if self.pattern_node.command.root_node.capture_group_references is None:
            self.pattern_node.command.root_node.capture_group_references = []

        if self.pattern_node.command.name not in self.pattern_node.command.root_node.capture_group_references:
            assert isinstance(self.pattern_node.command.name, str)
            self.pattern_node.command.root_node.capture_group_references.append(self.pattern_node.command.name)


class RegisterCaptureGroupProcessor:

    def __init__(self, pattern_node: PatternNodeTypeBuilder) -> None:
        self.pattern_node = pattern_node

    def process(self) -> PatternNodeTypes:
        return self.process_registry_capture_group()

    def process_registry_capture_group(self) -> PatternNodeTypes:
        if self.has_any_ancester_who_is_capture_group_reference_register():
            return PatternNodeTypes.capture_group_call_register

        self.add_new_references_to_global_list()

        # Decide which type of register capture group it is
        return SpecialRegisterCaptureGroupTypeDecider(pattern_node=self.pattern_node).process()

    def has_any_ancester_who_is_capture_group_reference_register(self) -> bool:
        "Check if any ancestor is a capture group reference"

        assert self.pattern_node.command.root_node
        pattern_node_name = self.pattern_node.command.name
        assert isinstance(pattern_node_name, str)

        main_reference_name = self.remove_access_suffix(pattern_node_name)

        assert hasattr(self.pattern_node.command.root_node, "capture_group_references")

        if self.pattern_node.command.root_node.capture_group_references is None:
            return False

        if main_reference_name in self.pattern_node.command.root_node.capture_group_references:
            return True
        return False

    @staticmethod
    def remove_access_suffix(pattern_name: str) -> str:
        "Remove the access suffix from the pattern name"

        parts = pattern_name.split(".")
        possible_register_suffix = [suffix.value for suffix in RegisterCaptureSuffixs]
        if parts[-1] in possible_register_suffix:
            return ".".join(parts[:-1])

        return pattern_name

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"
        assert self.pattern_node.command.root_node
        assert hasattr(self.pattern_node.command.root_node, "capture_group_references")

        if self.pattern_node.command.root_node.capture_group_references is None:
            self.pattern_node.command.root_node.capture_group_references = []

        assert isinstance(self.pattern_node.command.name, str)
        pattern_node_name_without_suffix = self.remove_access_suffix(self.pattern_node.command.name)

        if pattern_node_name_without_suffix not in self.pattern_node.command.root_node.capture_group_references:
            assert isinstance(pattern_node_name_without_suffix, str)
            self.pattern_node.command.root_node.capture_group_references.append(pattern_node_name_without_suffix)


class SpecialRegisterCaptureGroupTypeDecider:

    def __init__(self, pattern_node: PatternNodeTypeBuilder) -> None:
        self.pattern_node: PatternNodeTypeBuilder = pattern_node

        assert isinstance(pattern_node.command.name, str)
        self.pattern_name: str = pattern_node.command.name

    def process(self) -> PatternNodeTypes:
        return self._decide_and_process_capture_group_reference_register_based_on_type()

    def _decide_and_process_capture_group_reference_register_based_on_type(self) -> PatternNodeTypes:

        if self.is_genreg():
            return PatternNodeTypes.capture_group_reference_register_genreg
        if self.is_indreg():
            return PatternNodeTypes.capture_group_reference_register_indreg
        if self.is_stackreg():
            return PatternNodeTypes.capture_group_reference_register_stackreg
        if self.is_basereg():
            return PatternNodeTypes.capture_group_reference_register_basereg

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
