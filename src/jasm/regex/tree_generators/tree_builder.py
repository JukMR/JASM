from typing import List, Optional

from jasm.regex.pattern_node import PatternNode
from jasm.global_definitions import PatternNodeTypes, TimeType, dict_node


class PatternNodeBuilderNoParents:
    def __init__(self, command_dict: dict_node | str | int) -> None:
        self.command = command_dict

        # Check if is instance of int or str
        if isinstance(self.command, (int, str)):
            self.name = self.command
            self.times = TimeType(min_times=1, max_times=1)
            self.children = None

        elif isinstance(self.command, dict):
            self.name = self._get_name(self.command)
            self.times = self._get_times(self.command)
            self.children = self._get_children(name=self.name, command=self.command)

        # Case when PatternNode is from a deref
        elif isinstance(self.command, tuple):
            self.name = self.command[0]
            # self.time = self._get_times(self.command) # TODO: Fix this
            self.times = TimeType(min_times=1, max_times=1)
            self.children = self.get_simple_child(self.command[1])

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

            if isinstance(times, int):
                return TimeType(min_times=times, max_times=times)

            if isinstance(times, dict):
                min_time = times.get("min", 1)
                max_time = times.get("max", 1)
                return TimeType(min_times=min_time, max_times=max_time)

        return TimeType(min_times=1, max_times=1)

    @staticmethod
    def _get_children(name: str, command: dict_node) -> List[PatternNode]:
        assert isinstance(command, dict)

        if isinstance(command[name], List):
            return [PatternNodeBuilderNoParents(com).build() for com in command[name] if com != "times"]
        if isinstance(command[name], dict):
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
    def __init__(self, parent: PatternNode) -> None:
        assert isinstance(parent, PatternNode)
        self.command = parent

    def _get_type(self) -> PatternNodeTypes:
        if not getattr(self.command, "name", None):
            raise ValueError("Name is not defined")

        name = self.command.name

        if isinstance(name, str):
            if name == "$deref":
                return PatternNodeTypes.deref

            if self.is_father_is_deref():
                return PatternNodeTypes.deref_property

            if name.startswith("$"):
                if self.is_capture_group_reference(name[1:]):
                    return PatternNodeTypes.capture_group_reference

        # Is times
        if name == "times":
            return PatternNodeTypes.times

        # Is operand
        if isinstance(name, int):
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

    def is_father_is_deref(self) -> bool:
        "Check if the parent is a deref"
        if not self.command.parent:
            return False
        return self.command.parent.pattern_node_type == PatternNodeTypes.deref

    def any_ancestor_is_mnemonic(self) -> bool:
        "Check if any ancestor is a mnemonic"

        current_node = self.command.parent

        while current_node:
            if current_node.pattern_node_type == PatternNodeTypes.mnemonic:
                return True
            current_node = current_node.parent
        return False

    @staticmethod
    def is_capture_group_reference(name) -> bool:
        try:
            int(name)
            return True

        except ValueError:
            return False

    def build(self) -> None:
        self.set_type()
        if self.command.children:
            for child in self.command.children:
                PatternNodeTypeBuilder(child).build()
