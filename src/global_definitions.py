"Global definition file"

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, TypeAlias

SKIP_TO_END_OF_OPERAND = "[^,]*,"
SKIP_TO_END_OF_COMMAND = "[^|]*" + r"\|"
SKIP_TO_START_OF_OPERAND = "[^|,]*"
SKIP_TO_ANY_OPERAND_CHARS = "[^|]*"

IGNORE_INST_ADDR = r"[\dabcedf]+::"

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict

IncludeExcludeListType: TypeAlias = Optional[List[str]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]


class InputFileType(Enum):
    binary = auto()
    assembly = auto()


@dataclass
class TimeType:
    min: int
    max: int


dict_node: TypeAlias = Dict[str, Any] | str


class Command:
    def __init__(
        self, command_dict: dict_node, name: str, times: TimeType, children: Optional[List["Command"]]
    ) -> None:
        self.command_dict = command_dict
        self.name = name
        self.times = times
        self.children = children

    def get_regex(self, command: "Command") -> str:
        if command.is_leaf():
            return self.process_leaf(command)

        return self.process_branch(command)

    def is_leaf(self) -> bool:
        if isinstance(self.command_dict, int):
            return True
        if self.name == "pattern":
            return False

        return not self.name.startswith("$")

    def process_leaf(self, com: "Command") -> str:
        return self.form_regex_from_leaf(name=com.name, operands=com.children, times=com.times)

    def form_regex_from_leaf(self, name: str, operands: List[str], times: TimeType) -> str:
        operands_regex: str = self.get_operand_regex(operands)
        times_regex: str = self.get_min_max_regex(times)

        if operands_regex:
            return f"(({IGNORE_INST_ADDR}{name}{operands_regex}){times_regex})"
        return f"(({IGNORE_INST_ADDR}{name}{SKIP_TO_END_OF_OPERAND}){times_regex})"

    def process_branch(self, command: "Command") -> str:
        child_regexes = self.process_children(command)
        timex_regex: str = self.get_min_max_regex(times=command.times)

        match command.name:
            # Match case where command.name is and or pattern

            case "$and":
                return process_and(child_regexes, command=command, timex_regex=timex_regex)
            case "$or":
                return process_or(child_regexes, command=command, timex_regex=timex_regex)
            case "$not":
                return process_not(child_regexes, command=command, timex_regex=timex_regex)
            # case "$perm":
            #     return process_perm(child_regexes, command=command, timex_regex=timex_regex)
            case _:
                raise ValueError("Unknown command type")

    def process_children(self, command: "Command") -> List[str]:
        return [self.get_regex(child) for child in command.children]

    def get_min_max_regex(self, times: TimeType) -> str:
        return f"{{{times.min},{times.max}}}"

    def get_operand_regex(self, operands: Optional[List["Command"]] = None) -> Optional[str]:
        if not operands:
            return None
        return "".join(operand.get_regex(operand) for operand in operands)


def process_and(child_regexes: List[str], command: Command, timex_regex: str) -> str:
    return f"({''.join(child_regexes)}){timex_regex}"


def process_or(child_regexes: List[str], command: Command, timex_regex: str) -> str:
    return f"({join_instructions(child_regexes)}){timex_regex}"


@staticmethod
def join_instructions(inst_list: List[str]) -> str:
    "Join instructions from list using operand to generate regex"

    assert inst_list, "There are no instructions to join"

    regex_instructions = [f"{IGNORE_INST_ADDR}{elem}," for elem in inst_list]

    joined_by_bar_instructions = "|".join(regex_instructions)

    return joined_by_bar_instructions


def process_not(child_regexes: List[str], command: Command, timex_regex: str) -> str:
    times_regex: str = CommandProcessor().get_min_max_regex(times=command.times)

    return f"((?!{timex_regex}){SKIP_TO_END_OF_COMMAND}){times_regex}"


# def process_perm(child_regexes: List[str], command: Command, timex_regex: str) -> str:
#     return join_perm(regex)
