from typing import List

from src.global_definitions import Command, TimeType, dict_node, CommandTypes


class CommandBuilder:
    def __init__(self, command_dict: dict_node | str | int, parent: Command) -> None:
        self.command = command_dict
        self.parent = parent

        # Check if is instance of int or str
        if isinstance(command_dict, (int, str)):
            self.name = command_dict
            self.times = TimeType(min=1, max=1)
            self.children = None
            return

        if isinstance(command_dict, dict):
            self.name = self._get_name(command_dict)
            self.times = self._get_times(command_dict)
            self.children = self._get_children(name=self.name, command=command_dict)

        self.command_type = self._get_type()

    @staticmethod
    def _get_name(command_dict: dict_node) -> str:
        assert isinstance(command_dict, dict)
        return list(command_dict.keys())[0]

    @staticmethod
    def _get_times(command_dict: dict_node) -> TimeType:
        assert isinstance(command_dict, dict)
        times = command_dict.get("times", None)

        if isinstance(times, int):
            return TimeType(min=times, max=times)

        if isinstance(times, dict):
            return TimeType(min=times.get("min", 1), max=times.get("max", 1))

        return TimeType(min=1, max=1)

    @staticmethod
    def _get_children(name: str, command: dict_node) -> dict:
        assert isinstance(command, dict)

        # return [CommandBuilder(com, parent=).build() for com in command[name]]

    def _get_type(self) -> CommandTypes:
        if isinstance(self.name, int):
            return CommandTypes.operand

        if self.name.startswith("$"):
            return CommandTypes.node
        return CommandTypes.mnemonic

    def build(self) -> Command:
        assert isinstance(self.name, str)
        assert not isinstance(self.command, int)

        return Command(
            command_dict=self.command,
            name=self.name,
            times=self.times,
            children=self.children,
            parent=self.parent,
            command_type=self.command_type,
        )
