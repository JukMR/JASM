"Regex common functions module"

from typing import List


def list_without_last_character(string: str) -> str:
    "Return copy of string without last character"

    return string[:-1]


def join_instructions(inst_list: List[str], operand: str) -> str:
    "Join instructions from list using operand to generate regex"

    if len(inst_list) == 0:
        raise ValueError("There are no instructions to join")

    regex_instructions = [f"{elem},{operand}" for elem in inst_list]

    joined_by_bar_instructions = "|".join(regex_instructions)

    return joined_by_bar_instructions


def join_operands(operand_list: List[str], operand_ignore_number: str) -> str:
    "Join operands from list using operand_ignore_number to generate regex"

    if len(operand_list) == 0:
        raise ValueError("There are no operands to join")

    regex_operands = [rf"[^\|,]*{operand}{operand_ignore_number}" for operand in operand_list]

    joined_by_bar_operands = "|".join(regex_operands)

    return joined_by_bar_operands
