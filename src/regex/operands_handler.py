"Operands Regex generator module"

from typing import Any, Dict, List, Optional
from src.global_definitions import (
    IGNORE_OPERANDS_NUMBER,
    IGNORE_ARGS,
    SKIP_TO_END_COMMAND,
    IncludeExcludeListType,
    OperandListType,
    OperandType,
)
from src.regex.common_functions import join_operands


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

        joined_operand_include_list = join_operands(
            operand_list=operand_list, operand_ignore_number=IGNORE_OPERANDS_NUMBER
        )
        return joined_operand_include_list

    def _process_op_any(self, operand_elem: Dict[str, Any]):
        operand_include_list = operand_elem.get("include_list", None)
        operand_exclude_list = operand_elem.get("exclude_list", None)

        if operand_include_list is not None:
            operand_include_list = operand_include_list.get("ops", None)

        if operand_exclude_list is not None:
            operand_exclude_list = operand_exclude_list.get("ops", None)

        operand_include_list_regex = self._get_operand_list_or_regex(operand_include_list)
        operand_exclude_list_regex = self._get_operand_list_or_regex(operand_exclude_list)

        # Both None
        if operand_include_list_regex is None and operand_exclude_list_regex is None:
            # No operands. Probably should be enough checking for self.operands not to be None but just in case
            return f"{IGNORE_ARGS}"

        # Only include
        if operand_include_list_regex is not None and operand_exclude_list_regex is None:
            # Only include operands
            return f"{operand_include_list_regex}"

        # Only exclude
        if operand_include_list_regex is None and operand_exclude_list_regex is not None:
            # Only exclude operands
            return f"(?!{operand_exclude_list_regex}){IGNORE_ARGS}"

        # No none
        return f"(?!{operand_exclude_list_regex})({operand_include_list_regex})"

    def _process_not_any(self, operand_elem) -> str:
        operand_exclude_list = operand_elem.get("exclude_list", None)
        operand_exclude_list_regex = self._get_operand_list_or_regex(operand_exclude_list)

        only_exclude_regex = f"(?!{operand_exclude_list_regex}){IGNORE_ARGS}"
        return only_exclude_regex

    def _process_op_basic(self, operand_elem) -> str:
        only_single_op_regex = rf"([^,|]*{operand_elem}){{1}}[^,|]*,"
        return only_single_op_regex

    def _process_operand_elem(self, operand_elem: OperandType) -> str:
        if isinstance(operand_elem, Dict):
            keys = list(operand_elem.keys())
            if keys == ["$any"]:
                return self._process_op_any(operand_elem["$any"])
            if keys == ["$not"]:
                return self._process_not_any(operand_elem["$not"])
            if isinstance(keys[0], str):
                return self._process_op_basic(operand_elem)
            raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

        if isinstance(operand_elem, str):
            if operand_elem == "$any":
                return IGNORE_OPERANDS_NUMBER
            return rf"([^,|]*{operand_elem}{SKIP_TO_END_COMMAND}){{1}}"
        raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

    def get_regex(self) -> str:
        "Method to process operand and get operand regex"

        if self.operands is None:
            # If there's no operands specified then we assume it will be any number of them (including none).
            return IGNORE_ARGS

        operand_regex = [self._process_operand_elem(operand) for operand in self.operands]

        operand_regex_str = "".join(operand_regex)

        return operand_regex_str
