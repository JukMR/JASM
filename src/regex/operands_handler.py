"Operands Regex generator module"

from typing import Any, Dict, List, Optional
from src.global_definitions import (
    SKIP_TO_ANY_OPERAND_CHARS,
    SKIP_TO_END_OF_OPERAND,
    SKIP_TO_END_OF_COMMAND,
    IncludeExcludeListType,
    OperandListType,
    OperandType,
)


class OperandsHandler:
    "Class for handling the operand and creating the regex for it"

    def __init__(self, operands: OperandListType) -> None:
        self.operands = operands

    def _get_operand_list_or_regex(self, operand_list: IncludeExcludeListType) -> Optional[str]:
        "Returns the regex that matches all the posible operands"

        if operand_list is None:
            return None

        if not isinstance(operand_list, List):
            raise ValueError(f"operand_list : '{operand_list}' is not a List. It is a {type(operand_list)}")

        joined_operand_include_list_str = self.join_operands(
            operand_list=operand_list, operand_ignore_number=SKIP_TO_END_OF_OPERAND
        )
        return joined_operand_include_list_str

    def _process_op_any(self, operand_elem: Dict[str, Any]) -> str:
        operand_include_list = operand_elem.get("include_list", None)
        operand_exclude_list = operand_elem.get("exclude_list", None)

        operand_include_list_regex = self._get_operand_list_or_regex(operand_include_list)
        operand_exclude_list_regex = self._get_operand_list_or_regex(operand_exclude_list)

        # Both None
        if operand_include_list_regex is None and operand_exclude_list_regex is None:
            # No operands. Probably should be enough checking for self.operands not to be None but just in case
            return f"{SKIP_TO_END_OF_COMMAND}"

        # Only include
        if operand_include_list_regex is not None and operand_exclude_list_regex is None:
            # Only include operands
            return f"{operand_include_list_regex}"

        # Only exclude
        if operand_include_list_regex is None and operand_exclude_list_regex is not None:
            # Only exclude operands
            return f"(?!{operand_exclude_list_regex}){SKIP_TO_END_OF_COMMAND}"

        # No none
        return f"(?!{operand_exclude_list_regex})({operand_include_list_regex})"

    def _process_op_not(self, operand_elem) -> str:
        operand_exclude_list = operand_elem.get("exclude_list", None)
        operand_exclude_list_regex = self._get_operand_list_or_regex(operand_exclude_list)

        only_exclude_regex = f"(?!{operand_exclude_list_regex}){SKIP_TO_END_OF_COMMAND}"
        return only_exclude_regex

    def _process_op_basic(self, operand_elem) -> str:
        only_single_op_regex = rf"([^,|]*{operand_elem}){{1}}[^,|]*,"
        return only_single_op_regex

    def _process_operand_elem(self, operand_elem: OperandType) -> str:
        if isinstance(operand_elem, Dict):
            keys = list(operand_elem.keys())
            if keys == ["$or"]:
                return self._process_op_any(operand_elem["$or"])
            if keys == ["$not"]:
                return self._process_op_not(operand_elem["$not"])
            if isinstance(keys[0], str):
                if isinstance(operand_elem, Dict):
                    raise ValueError(f"operand_elem is of type Dict: {operand_elem}")
                return self._process_op_basic(operand_elem)
            raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

        if isinstance(operand_elem, (int, str)):
            if operand_elem == "$or":
                return SKIP_TO_END_OF_OPERAND
            return rf"([^,|]*{operand_elem}){{1}}{SKIP_TO_END_OF_OPERAND}"
        raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

    def join_operands(self, operand_list: List[str], operand_ignore_number: str) -> str:
        "Join operands from list using operand_ignore_number to generate regex"

        if len(operand_list) == 0:
            raise ValueError("There are no operands to join")

        regex_operands = [f"{SKIP_TO_ANY_OPERAND_CHARS}{operand}{operand_ignore_number}" for operand in operand_list]

        joined_by_bar_operands = "|".join(regex_operands)

        return f"{joined_by_bar_operands}"

    def get_regex(self) -> str:
        "Method to process operand and get operand regex"

        if self.operands is None:
            # If there's no operands specified then we assume it will be any number of them (including none).
            return SKIP_TO_END_OF_COMMAND

        operand_regex = [self._process_operand_elem(operand) for operand in self.operands]

        operand_regex_str = "".join(operand_regex) + SKIP_TO_END_OF_COMMAND

        return operand_regex_str
