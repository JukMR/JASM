from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from outer import process_times, process_and, process_or, process_not, process_perm


@dataclass
class Command:
    command: Dict[str, Any]
    name: str
    times: str
    children: Optional[Dict[str, "Command"]] | Optional[List["Command"]]

    def is_leaf(self) -> bool:
        return not self.name.startswith("$")


class CommandBuilder:
    def __init__(self, command: Dict[str, Any]):
        self.command = command

        self.name = self._get_name()
        self.times = self._get_times()
        self.children = self._get_children()

    def _get_name(self) -> str:
        return list(self.command.keys())[0]

    def _get_times(self) -> str:
        times = self.command.get("times", None)
        if not times:
            return "{1}"

        return process_times(times)

    def _get_children(self) -> List[Dict[str, "Command"]]:
        return self.command.values()

    def build(self) -> Command:
        return Command(command=self.command, name=self.name, times=self.times, children=self.children)


class CommandProcessor:
    def process_command(self, command: Command):
        if command.is_leaf():
            return self._process_leaf(command)

        childs = command.children
        strings: List[str] = self._process_childs(childs)
        return self.process_based_on_command_type(command)

    def _process_childs(self, childs: Command) -> List[str]:
        return [self.process_command(child) for child in childs]

    @staticmethod
    def _process_leaf(com: Command) -> str:
        return form_regex(name=com.name, operands=com.children, times=com.times)

    @staticmethod
    def process_based_on_command_type(command) -> str:
        match command.name:
            case "$and":
                return process_and(command)
            case "$or":
                return process_or(command)
            case "$not":
                return process_not(command)
            case "$perm":
                return process_perm(command)
            case _:
                raise ValueError("Unknown command type")


def form_regex(name: str, operands: List[Dict[str, Any]], times: str) -> str:
    """TODO: implement this"""
    return ""
