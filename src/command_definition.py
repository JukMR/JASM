"Global definition file"

from typing import List, Optional

from src.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    COMMA,
    IGNORE_INST_ADDR,
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    SKIP_TO_END_OF_COMMAND,
    SKIP_TO_END_OF_OPERAND,
    CommandTypes,
    TimeType,
    dict_node,
)


class Command:
    def __init__(
        self,
        command_dict: dict_node,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["Command"]],
        command_type: Optional[CommandTypes],
        parent: Optional["Command"],
    ) -> None:
        self.command_dict = command_dict
        self.name = name
        self.times = times
        self.children = children
        self.command_type = command_type
        self.parent = parent

    def get_regex(self, command: "Command") -> str:
        if command.command_type in [CommandTypes.mnemonic, CommandTypes.operand]:
            return self.process_leaf(command)
        return self.process_branch(command)

    def process_leaf(self, com: "Command") -> str:
        return f"{self.form_regex_from_leaf(com)}"

    def form_regex_from_leaf(self, com: "Command") -> str | int:
        name = com.name
        children = com.children
        times = com.times
        if not children:
            if com.command_type == CommandTypes.operand:
                # Is an operand
                return self.sanitize_operand_name(name)
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

        operand_name: str | int
        if ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS:
            operand_name = f"{IGNORE_NAME_PREFIX}{name}{IGNORE_NAME_SUFFIX}"
        else:
            operand_name = name

        return operand_name

    def process_branch(self, command: "Command") -> str:
        child_regexes = self.process_children(command)
        times_regex: Optional[str] = global_get_min_max_regex(times=command.times)

        match command.name:
            # Match case where command.name is and or pattern

            case "$and":
                return BranchProcessor().process_and(child_regexes, times_regex=times_regex)
            case "$or":
                return BranchProcessor().process_or(child_regexes, times_regex=times_regex)
            case "$not":
                return BranchProcessor().process_not(child_regexes, times_regex=times_regex)
            # case "$perm":
            #     return BranchProcessor().process_perm(child_regexes, times_regex=times_regex)
            # case "$any_order":
            #     return BranchProcessor().process_any_order(child_regexes, times_regex=times_regex)
            case _:
                raise ValueError("Unknown command type")

    def process_children(self, command: "Command") -> List[str]:
        if command.children:
            return [self.get_regex(child) for child in command.children]
        raise ValueError("Children list is empty")


class RegexWithOperandsCreator:
    def __init__(self, name: str | int, operands: Optional[List[Command]], times: Optional[TimeType]) -> None:
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

        return (
            SKIP_TO_END_OF_OPERAND.join(operand.get_regex(operand) for operand in self.operands)
            + SKIP_TO_END_OF_OPERAND
        )

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None
        return global_get_min_max_regex(times=self.times)

    def _form_regex_with_time(self, operands_regex: Optional[str], times_regex: str) -> str:
        # Add prefix and suffix to name to allow matching only substring
        command_name: str | int

        if ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS:
            command_name = f"{IGNORE_NAME_PREFIX}{self.name}{IGNORE_NAME_SUFFIX}"
        else:
            command_name = self.name

        if operands_regex:
            return f"(({IGNORE_INST_ADDR}{command_name}({operands_regex})){times_regex})"
        return f"(({IGNORE_INST_ADDR}{command_name}{SKIP_TO_END_OF_COMMAND}){times_regex})"

    def _form_regex_without_time(self, operands_regex: Optional[str]) -> str:
        command_name: str | int
        if ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS:
            command_name = f"{IGNORE_NAME_PREFIX}{self.name}{IGNORE_NAME_SUFFIX}"
        else:
            command_name = self.name

        if operands_regex:
            return f"({IGNORE_INST_ADDR}{command_name}{operands_regex}{SKIP_TO_END_OF_COMMAND})"
        return f"({IGNORE_INST_ADDR}{command_name}{SKIP_TO_END_OF_COMMAND})"


class BranchProcessor:
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

    # @staticmethod
    # def process_any_order(child_regexes: List[str], times_regex: Optional[str]) -> str:
    #     # TODO: implement this
    #     return ""

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