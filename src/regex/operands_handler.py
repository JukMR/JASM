"Operands Regex generator module"

from typing import List, Optional
from src.global_definitions import IGNORE_OPERANDS_NUMBER, IGNORE_ARGS, IncludeExcludeListType, OperandType
from src.regex.common_functions import join_operands


class OperandsHandler:
    "Class for handling the operand and creating the regex for it"

    def __init__(self, operands: OperandType) -> None:
        self.operands = operands

    def _get_operand_list_or_regex(self, operand_list: IncludeExcludeListType) -> Optional[str]:
        "Returns the regex that matches all the posible operands"

        if operand_list is None:
            return None

        if not isinstance(operand_list, List):
            raise ValueError(f"operand_list : '{operand_list}' is not a List. It is a {type(operand_list)}")

        joined_operand_include_list = join_operands(
            operand_list=operand_list, operand_ignore_number=IGNORE_OPERANDS_NUMBER
        )
        return joined_operand_include_list

    def get_regex(self) -> str:
        "Method to process operand and get operand regex"

        if self.operands is None:
            # If there's no operands specified then we assume it will be any number of them (including none).
            return IGNORE_ARGS

        operand_include_list = self.operands.get("include_list", None)
        operand_exclude_list = self.operands.get("exclude_list", None)

        if operand_include_list is not None:
            operand_include_list = operand_include_list.get("inst", None)

        if operand_exclude_list is not None:
            operand_exclude_list = operand_exclude_list.get("inst", None)

        operand_include_list_regex = self._get_operand_list_or_regex(operand_include_list)
        operand_exclude_list_regex = self._get_operand_list_or_regex(operand_exclude_list)

        # Both None
        if operand_include_list_regex is None and operand_exclude_list_regex is None:
            # No operands. Probably should be enough checking for self.operands not to be None but just in case
            return f"{IGNORE_ARGS}"

        # Only exclude None
        if operand_include_list_regex is not None and operand_exclude_list_regex is None:
            # Only include operands
            return f"{operand_include_list_regex}+"

        # Only include None
        if operand_include_list_regex is None and operand_exclude_list_regex is not None:
            # Only exclude operands
            return f"(?!{operand_exclude_list_regex}){IGNORE_ARGS}"

        # Both not None
        return f"(?!{operand_exclude_list_regex})({operand_include_list_regex})+"
