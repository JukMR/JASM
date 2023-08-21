'Operands Regex generator module'

from typing import Optional
from src.global_definitions import IGNORE_OPERANDS_NUMBER, IGNORE_ARGS, IncludeExcludeListType, OperandType
from src.regex.common_functions import join_instructions, list_without_last_character


class OperandsHandler():
    'Class for handling the operand and creating the regex for it'

    def __init__(self, operands: OperandType) -> None:
        self.operands = operands

    def get_operand_list_or_regex(self, operand_list: IncludeExcludeListType) -> Optional[str]:
        "Returns the regex that matches all the posible operands"

        if operand_list is None:
            return None
        joined_operand_include_list = join_instructions(inst_list=operand_list, ignore_pattern=IGNORE_OPERANDS_NUMBER)
        return list_without_last_character(joined_operand_include_list)

    def get_regex(self) -> str:
        'Method to process operand and get operand regex'

        if self.operands is None:
            # If there's no operands specified then we assume it will be any number of them (including none).
            return IGNORE_ARGS

        operand_include_list = self.operands.get('include_list', None)
        operand_exclude_list = self.operands.get('exclude_list', None)

        operand_include_list_regex = self.get_operand_list_or_regex(operand_include_list)
        operand_exclude_list_regex = self.get_operand_list_or_regex(operand_exclude_list)

        if operand_exclude_list is None and operand_exclude_list_regex is None:
            # No operands. Probably should be enough checking for self.operands not to be None but just in case
            return f"{IGNORE_ARGS}"

        if operand_include_list_regex is not None and operand_exclude_list_regex is None:
            # Only include operands
            return f"{operand_include_list_regex}"

        if operand_exclude_list_regex is not None and operand_include_list_regex is None:
            # Only exclude operands
            return f"(?!{operand_exclude_list_regex}){IGNORE_ARGS}"

        return f"(?!{operand_exclude_list_regex})({operand_include_list_regex})"
