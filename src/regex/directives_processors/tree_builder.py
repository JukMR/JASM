from typing import List

from src.global_definitions import Command, TimeType, dict_node


class CommandBuilder:
    def __init__(self, command_dict: dict_node | str | int) -> None:
        self.command = command_dict

        # Check if is instance of int or str
        if isinstance(command_dict, (int, str)):
            self.name = command_dict
            self.times = TimeType(min=1, max=1)
            self.children = None
            return

        if isinstance(command_dict, dict):
            self.name = self._get_name(command_dict)
            self.times = self._get_times(command_dict)
            self.children = self.get_children(name=self.name, command=command_dict)

    @staticmethod
    def _get_name(command_dict: dict_node) -> str:
        return list(command_dict.keys())[0]

    @staticmethod
    def _get_times(command_dict: dict_node) -> TimeType:
        times = command_dict.get("times", None)

        if isinstance(times, int):
            return TimeType(min=times, max=times)

        if isinstance(times, dict):
            return TimeType(min=times.get("min", 1), max=times.get("max", 1))

        return TimeType(min=1, max=1)

    @staticmethod
    def get_children(name: str, command: dict_node) -> List[Command]:
        return [CommandBuilder(com).build() for com in command[name]]

    def build(self) -> Command:
        return Command(command_dict=self.command, name=self.name, times=self.times, children=self.children)
