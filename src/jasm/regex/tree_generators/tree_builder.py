from typing import List, Optional

from jasm.global_definitions import PatternNodeTypes, TimeType, dict_node
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeBuilderNoParents:
    def __init__(self, command_dict: dict_node) -> None:
        self.command = command_dict

        # Check if is instance of int or str
        match self.command:
            case int() | str():
                self.name = self.command
                self.times = TimeType(min_times=1, max_times=1)
                self.children = None

            case dict():
                self.name = self._get_name(self.command)
                self.times = self._get_times(self.command)
                self.children = self._get_children(name=self.name, command=self.command)

            # Case when PatternNode is from a deref
            case tuple():
                self.name = self.command[0]
                # self.time = self._get_times(self.command) # TODO: Fix this
                self.times = TimeType(min_times=1, max_times=1)
                self.children = self.get_simple_child(self.command[1])

            case _:
                raise ValueError(f"Command {self.command} is not a valid type")

    @staticmethod
    def _get_name(command_dict: dict_node) -> str:
        assert isinstance(command_dict, dict)
        return list(command_dict.keys())[0]

    def _get_times(self, command_dict: dict_node) -> TimeType:
        assert isinstance(command_dict, dict)

        def _get_time_object(command_dict: dict) -> Optional[dict]:
            command_name = list(command_dict.keys())[0]

            # Command has no operands, only a time
            if "times" in command_dict.keys():
                return command_dict.get("times")

            # Command has operands and a time
            if "times" in command_dict[command_name]:
                return command_dict[command_name].get("times")
            return None

        if isinstance(command_dict, dict):
            times = _get_time_object(command_dict)

            match times:
                case int():
                    return TimeType(min_times=times, max_times=times)

                case dict():
                    min_time = times.get("min", 1)
                    max_time = times.get("max", 1)
                    return TimeType(min_times=min_time, max_times=max_time)

        return TimeType(min_times=1, max_times=1)

    @staticmethod
    def _get_children(name: str, command: dict_node) -> List[PatternNode]:
        assert isinstance(command, dict)

        match command[name]:
            case list():
                return [PatternNodeBuilderNoParents(com).build() for com in command[name] if com != "times"]
            case dict():
                return [PatternNodeBuilderNoParents(com).build() for com in command[name].items() if com != "times"]

        raise ValueError("Command is not a list or a dict")

    @staticmethod
    def get_simple_child(name: str) -> List[PatternNode]:
        return [
            PatternNode(
                name=name,
                times=TimeType(min_times=1, max_times=1),
                children=None,
                pattern_node_dict=name,
                pattern_node_type=PatternNodeTypes.deref_property,
                parent=None,
            )
        ]

    def build(self) -> PatternNode:
        assert isinstance(self.name, (str, int))

        return PatternNode(
            pattern_node_dict=self.command,
            name=self.name,
            times=self.times,
            children=self.children,
            pattern_node_type=None,
            parent=None,
        )


class PatternNodeParentsBuilder:
    def __init__(self, command: PatternNode) -> None:
        self.command = command

    def set_parent(self, parent: PatternNode, children: List[PatternNode]) -> None:
        for child in children:
            child.parent = parent
            if child.children:  # Recursively set parent for the child's children
                assert isinstance(child.children, (List, str))
                self.set_parent(child, child.children)

    def build(self) -> None:
        if self.command.children:
            assert isinstance(self.command.children, List)
            self.set_parent(self.command, self.command.children)


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
        if self.command.name in self.command.capture_group_references:
            return True
        return False

    def add_new_references_to_global_list(self) -> None:
        "Add new references to global list"

        if self.command.name not in self.command.capture_group_references:
            assert isinstance(self.command.name, str)
            self.command.capture_group_references.append(self.command.name)

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
        if self.command.children:
            for child in self.command.children:
                PatternNodeTypeBuilder(child).build()
