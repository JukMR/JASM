from typing import List

from src.global_definitions import Command, CommandTypes, TimeType, dict_node


class CommandBuilderNoParents:
    def __init__(self, command_dict: dict_node | str | int) -> None:
        self.command = command_dict
        self.parent = None

        # Check if is instance of int or str
        if isinstance(command_dict, (int, str)):
            self.name = command_dict
            self.times = TimeType(min=1, max=1)
            self.children = None

        elif isinstance(command_dict, dict):
            self.name = self._get_name(command_dict)
            self.times = self._get_times(command_dict)
            self.children = self._get_children(name=self.name, command=command_dict)

    @staticmethod
    def _get_name(command_dict: dict_node) -> str:
        assert isinstance(command_dict, dict)
        return list(command_dict.keys())[0]

    @staticmethod
    def _get_times(command_dict: dict_node) -> TimeType:
        assert isinstance(command_dict, dict)

        if isinstance(command_dict, dict) and "times" in command_dict.keys():
            times = command_dict.get("times")

            if isinstance(times, int):
                return TimeType(min=times, max=times)

            if isinstance(times, dict):
                return TimeType(min=times.get("min", 1), max=times.get("max", 1))

        return TimeType(min=1, max=1)

    def _get_children(self, name: str, command: dict_node) -> List[Command]:
        assert isinstance(command, dict)
        assert isinstance(self.command, dict)

        return [CommandBuilderNoParents(com).build() for com in command[name] if com != "times"]

    def build(self) -> Command:
        assert isinstance(self.name, (str, int))
        # assert not isinstance(self.command, int)

        return Command(
            command_dict=self.command,
            name=self.name,
            times=self.times,
            children=self.children,
            parent=self.parent,
            command_type=None,
        )


class CommandParentsBuilder:
    def __init__(self, command: Command) -> None:
        self.command = command

    def set_parent(self, parent: Command, children: List[Command]) -> None:
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
    def __init__(self, parent: Command) -> None:
        self.command = parent

    def _get_type(self) -> CommandTypes:
        if not getattr(self.command, "name", None):
            raise ValueError("Name is not defined")

        # Is operand
        if isinstance(self.command.name, int) or self.is_father_is_mnemonic():
            return CommandTypes.operand

        # Is node
        if self.command.name.startswith("$"):
            return CommandTypes.node

        # Else is mnemonic
        return CommandTypes.mnemonic

    def set_type(self) -> Command:
        self.command.command_type = self._get_type()
        return self.command

    def is_father_is_mnemonic(self) -> bool:
        # Check if the parent is a mnemonic
        assert isinstance(self.command, Command)

        if not self.command.parent:
            return False
        return self.command.parent.command_type == CommandTypes.mnemonic

    def build(self) -> None:
        self.set_type()
        if self.command.children:
            for child in self.command.children:
                CommandsTypeBuilder(child).build()
