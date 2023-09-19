"Instruction Processor Module"

from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from src.global_definitions import MAX_PYTHON_INT
from src.global_definitions import (
    PatternDict,
    IncludeExcludeListType,
    TimesType,
    OperandListType,
)


class IDirectiveProcessor(ABC):
    """Interface Directive Processor for the Strategy Pattern"""

    def __init__(
        self,
        pattern: PatternDict,
        include_list: IncludeExcludeListType,
        exclude_list: IncludeExcludeListType,
        times: TimesType,
        operands: OperandListType,
    ) -> None:
        self.pattern = pattern
        self.include_list = include_list
        self.exclude_list = exclude_list
        self.times = times
        self.operands = operands

    @staticmethod
    def get_times(pattern: PatternDict) -> TimesType:
        "Get `times` from pattern or None"
        return pattern.get("times", None)

    def _get_min_max_regex(self) -> Optional[str]:
        if self.times is None:
            return None

        assert isinstance(self.times, Dict), f"times property inside {self.pattern} is not a Dict"

        min_amount = self.times.get("min", 1)
        max_amount = self.times.get("max", MAX_PYTHON_INT)

        assert min_amount <= max_amount, f"Wrong min:{min_amount} or max:{max_amount} in directive"

        return f"{{{min_amount},{max_amount}}}"

    @staticmethod
    def join_instructions(inst_list: List[str], operand: str) -> str:
        "Join instructions from list using operand to generate regex"

        assert len(inst_list) != 0, "There are no instructions to join"

        regex_instructions = [f"{elem},{operand}" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions

    @abstractmethod
    def process(self) -> str:
        "Method for parsing instruction from given assembly"
