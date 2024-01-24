"Command definition file"

from itertools import permutations
from typing import List, Optional

from src.jasm.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    IGNORE_INST_ADDR,
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    SKIP_TO_END_OF_COMMAND,
    CommandTypes,
    TimeType,
    dict_node,
)


def get_command_name(
    name: str | int,
    allow_matching_substrings: bool = ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    name_prefix: str = IGNORE_NAME_PREFIX,
    name_suffix: str = IGNORE_NAME_SUFFIX,
) -> str | int:
    if name == "@any":
        name = "[^,]*"
    if allow_matching_substrings:
        return f"{name_prefix}{name}{name_suffix}"
    return name


class PatternNode:
    def __init__(
        self,
        command_dict: dict_node,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["PatternNode"]],
        command_type: Optional[CommandTypes],
        parent: Optional["PatternNode"],
    ) -> None:
        """
        Initialize a Command object.

        :param command_dict: A dictionary representing the command structure.
        :param name: The name of the command.
        :param times: Repeating information for the command execution.
        :param children: Sub-commands or child commands.
        :param command_type: The type of the command (mnemonic, operand, etc.).
        :param parent: The parent command, if any.
        """
        self.command_dict = command_dict
        self.name = name
        self.times = times
        self.children = children
        self.command_type = command_type
        self.parent = parent

    def get_regex(self, command: "PatternNode") -> str:
        if command.command_type in [CommandTypes.mnemonic, CommandTypes.operand]:
            return self.process_leaf(command)
        return self.process_branch(command)

    def process_leaf(self, com: "PatternNode") -> str:
        name = com.name
        children = com.children
        times = com.times
        if not children:
            if com.command_type == CommandTypes.operand:
                # Is an operand
                return str(self.sanitize_operand_name(name))
            # Is a mnemonic with no operands
            print(f"Found a mnemonic with no operands: {com.name}")

        assert isinstance(children, List) or (not children), "Children must be a list or None"
        return RegexWithOperandsCreator(name=name, operands=children, times=times).generate_regex()

    def sanitize_operand_name(self, name: str | int) -> str | int:
        def _is_hex_operand(name: str | int) -> bool:
            if isinstance(name, int):
                return False
            if name.endswith("h"):
                tmp = name.removesuffix("h")
                try:
                    int(tmp, base=16)
                    return True
                except ValueError:
                    return False
            return False

        if _is_hex_operand(name):

            def _process_hex_operand(hex_operand_elem: str) -> str:
                operand_elem = "0x" + hex_operand_elem.removesuffix("h")
                return operand_elem

            # Match hex operand
            assert isinstance(name, str), "Operand name must be a string"
            return _process_hex_operand(name)

        command_name = get_command_name(name)
        return command_name

    def process_branch(self, command: "PatternNode") -> str:
        child_regexes = self.process_children(command)
        times_regex: Optional[str] = global_get_min_max_regex(times=command.times)
        return BranchProcessor().process_command(command.name, child_regexes, times_regex)

    def process_children(self, command: "PatternNode") -> List[str]:
        if command.children:
            return [self.get_regex(child) for child in command.children]
        raise ValueError("Children list is empty")


class RegexWithOperandsCreator:
    def __init__(self, name: str | int, operands: Optional[List[PatternNode]], times: Optional[TimeType]) -> None:
        self.name = name
        self.operands = operands
        self.times = times

    def generate_regex(self) -> str:
        operands_regex: Optional[str] = self.get_operand_regex()
        times_regex: Optional[str] = self.get_min_max_regex()

        if times_regex:
            return self._form_regex_with_time(operands_regex=operands_regex, times_regex=times_regex)
        return self._form_regex_without_time(operands_regex=operands_regex)

    def get_operand_regex(self) -> Optional[str]:
        if not self.operands:
            return None

        return "".join(operand.get_regex(operand) for operand in self.operands)

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None
        return global_get_min_max_regex(times=self.times)

    def _form_regex_with_time(self, operands_regex: Optional[str], times_regex: str) -> str:
        # Add prefix and suffix to name to allow matching only substring
        command_name = get_command_name(self.name)

        if operands_regex:
            return f"(({IGNORE_INST_ADDR}{command_name}({operands_regex}){SKIP_TO_END_OF_COMMAND}){times_regex})"
        return f"(({IGNORE_INST_ADDR}{command_name}{SKIP_TO_END_OF_COMMAND}){times_regex})"

    def _form_regex_without_time(self, operands_regex: Optional[str]) -> str:
        command_name = get_command_name(self.name)

        if operands_regex:
            return f"({IGNORE_INST_ADDR}{command_name}{operands_regex}{SKIP_TO_END_OF_COMMAND})"
        return f"({IGNORE_INST_ADDR}{command_name}{SKIP_TO_END_OF_COMMAND})"


class BranchProcessor:
    def process_command(self, command_name: str | int, child_regexes: List[str], times_regex: Optional[str]) -> str:
        """
        Process a command based on its name and child regexes.

        :param command_name: The name of the command.
        :param child_regexes: List of regexes from child commands.
        :param times_regex: The regex string for repeating the match.
        :return: The processed command regex.
        """
        match command_name:
            # Match case where command.name is and or pattern

            case "$and":
                return self.process_and(child_regexes, times_regex=times_regex)
            case "$or":
                return self.process_or(child_regexes, times_regex=times_regex)
            case "$not":
                return self.process_not(child_regexes, times_regex=times_regex)
            # case "$perm":
            #     return self.process_perm(child_regexes, times_regex=times_regex)
            case "$and_any_order":
                return self.process_and_any_order(child_regexes, times_regex=times_regex)
            case _:
                raise ValueError("Unknown command type")

    @staticmethod
    def process_and(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"({''.join(child_regexes) + SKIP_TO_END_OF_COMMAND}){times_regex}"
        return f"({''.join(child_regexes)})"

    def process_or(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"({self.join_instructions(child_regexes)}){times_regex}"
        return f"({self.join_instructions(child_regexes)})"

    @staticmethod
    def process_not(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"((?!{''.join(child_regexes)}){SKIP_TO_END_OF_COMMAND}){times_regex}"
        return f"((?!{''.join(child_regexes)}){SKIP_TO_END_OF_COMMAND})"

    # @staticmethod
    # def process_perm(child_regexes: List[str], times_regex: Optional[str]) -> str:
    #     # TODO: implement this
    #     return ""

    def process_and_any_order(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        full_all_against_all_regex: List[List[str]] = self.generate_any_order_permutation(child_regexes)

        regex_list: List[str] = []
        for list_regex in full_all_against_all_regex:
            regex_list.append(self.process_and(child_regexes=list_regex, times_regex=None))

        return self.process_or(regex_list, times_regex)

    @staticmethod
    def generate_any_order_permutation(child_regexes: List[str]) -> List[List[str]]:
        # Generate all the permutation of this list
        return [list(permutation) for permutation in permutations(child_regexes)]

    @staticmethod
    def join_instructions(inst_list: List[str]) -> str:
        "Join instructions from list using operand to generate regex"

        assert inst_list, "There are no instructions to join"

        regex_instructions = [f"({elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions


def global_get_min_max_regex(times: TimeType) -> Optional[str]:
    if times.min_times == 1 and times.max_times == 1:
        return None
    if times.min_times == times.max_times:
        return f"{{{times.min_times}}}"
    return f"{{{times.min_times},{times.max_times}}}"
