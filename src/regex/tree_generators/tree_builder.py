from typing import List, Optional

from src.regex.command import PatternNode
from src.global_definitions import CommandTypes, TimeType, dict_node


class CommandBuilderNoParents:
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

        return [CommandBuilderNoParents(com).build() for com in command[name] if com != "times"]

    def build(self) -> PatternNode:
        assert isinstance(self.name, (str, int))

        return PatternNode(
            command_dict=self.command,
            name=self.name,
            times=self.times,
            children=self.children,
            parent=None,
            command_type=None,
        )


class CommandParentsBuilder:
    def __init__(self, command: PatternNode) -> None:
        self.command = command

    def set_parent(self, parent: PatternNode, children: List[PatternNode]) -> None:
        for child in children:
            child.parent = parent
            if child.children:  # Recursively set parent for the child's children
                assert isinstance(child.children, List)
                self.set_parent(child, child.children)

    def build(self) -> None:
        if self.command.children:
            assert isinstance(self.command.children, List)
            self.set_parent(self.command, self.command.children)


class CommandsTypeBuilder:
    def __init__(self, parent: PatternNode) -> None:
        assert isinstance(parent, PatternNode)
        self.command = parent

    def _get_type(self) -> CommandTypes:
        if not getattr(self.command, "name", None):
            raise ValueError("Name is not defined")

        name = self.command.name

        # Is operand

        if isinstance(name, int):
            return CommandTypes.operand

        # Is node
        if name.startswith("$"):
            return CommandTypes.node

        if self.is_father_is_mnemonic():
            return CommandTypes.operand

        if self.any_ancestor_is_mnemonic():
            return CommandTypes.operand

        # Else is mnemonic
        return CommandTypes.mnemonic

    def set_type(self) -> PatternNode:
        self.command.command_type = self._get_type()
        return self.command

    def is_father_is_mnemonic(self) -> bool:
        "Check if the parent is a mnemonic"
        if not self.command.parent:
            return False
        return self.command.parent.command_type == CommandTypes.mnemonic

    def any_ancestor_is_mnemonic(self) -> bool:
        "Check if any ancestor is a mnemonic"

        current_node = self.command.parent

        while current_node:
            if current_node.command_type == CommandTypes.mnemonic:
                return True
            current_node = current_node.parent
        return False

    def build(self) -> None:
        self.set_type()
        if self.command.children:
            for child in self.command.children:
                CommandsTypeBuilder(child).build()
