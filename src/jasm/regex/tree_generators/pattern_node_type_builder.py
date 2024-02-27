from jasm.global_definitions import PatternNodeTypes
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeTypeBuilder:
    def __init__(self, pattern_node: PatternNode) -> None:
        assert isinstance(pattern_node, PatternNode)
        self.command = pattern_node

    def _get_type(self) -> PatternNodeTypes:
        if getattr(self.command, "name", None) is None:
            raise ValueError("Name is not defined")

        name = self.command.name

        if isinstance(name, str):
            # DEREF TYPES
            if name == "$deref":
                return PatternNodeTypes.deref

            if self.is_ancestor_deref():
                if self.is_deref_property_capture_group():

                    if self.has_any_ancester_who_is_capture_group_reference():
                        return PatternNodeTypes.deref_property_capture_group_call

                    self.add_new_references_to_global_list()
                    return PatternNodeTypes.deref_property_capture_group_reference
                return PatternNodeTypes.deref_property

            # CAPTURE GROUP TYPES
            # Is a capture group reference
            if name.startswith("&"):

                # Is Capture Group in operand
                if self.is_capture_group_operand():
                    if self.has_any_ancester_who_is_capture_group_reference():
                        return PatternNodeTypes.capture_group_call_operand

                    self.add_new_references_to_global_list()
                    return PatternNodeTypes.capture_group_reference_operand

                # Is Capture Group in Mnemonic
                # Add this macro to refence list
                # First check it it should be a new reference or a call to an existing one
                if self.has_any_ancester_who_is_capture_group_reference():
                    # This is the using the reference
                    return PatternNodeTypes.capture_group_call

                # This is creating the reference
                self.add_new_references_to_global_list()
                return PatternNodeTypes.capture_group_reference

        # Is times
        if name == "times":
            return PatternNodeTypes.times

        # Is operand
        if isinstance(name, int):
            if self.is_ancestor_deref():
                return PatternNodeTypes.deref_property
            return PatternNodeTypes.operand

        # Is root node
        if self.command.parent is None:
            return PatternNodeTypes.root

        # Is node
        if self.is_node(name):
            return PatternNodeTypes.node

        if self.is_father_is_mnemonic():
            return PatternNodeTypes.operand

        if self.any_ancestor_is_mnemonic():
            return PatternNodeTypes.operand

        # Else is mnemonic
        return PatternNodeTypes.mnemonic

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

    def is_capture_group_operand(self) -> bool:
        "Check if the current node is a capture group operand"
        if not self.command.parent:
            return False

        if self.command.parent.pattern_node_type == PatternNodeTypes.mnemonic:
            return True

        return False

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
