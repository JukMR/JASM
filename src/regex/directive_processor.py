'Instruction Processor Module'

from dataclasses import dataclass
from typing import List, Dict, Optional

from src.global_definitions import IGNORE_ARGS, MAX_PYTHON_INT
from src.global_definitions import PatternDict, IncludeExcludeListType, TimesType, OperandType
from src.regex.common_functions import join_instructions
from src.regex.operands_handler import OperandsHandler


@dataclass
class DirectiveProcessor:
    'Instruction Processor'

    pattern: PatternDict
    include_list: IncludeExcludeListType
    exclude_list: IncludeExcludeListType
    times: TimesType
    operands: OperandType


    @staticmethod
    def _generate_only_include(include_list_regex: List[str], times_regex: Optional[str]) -> str:
        inst_joined = join_instructions(inst_list=include_list_regex, ignore_pattern=IGNORE_ARGS)

        if times_regex is None:
            return f"({inst_joined})"

        return f"({inst_joined}){times_regex}"


    @staticmethod
    def _generate_only_exclude(exclude_list_regex: List[str], times_regex: Optional[str]) -> str:
        inst_joined = join_instructions(inst_list=exclude_list_regex, ignore_pattern=IGNORE_ARGS)

        if times_regex is None:
            return f"((?!{inst_joined}){IGNORE_ARGS})"

        return f"((?!{inst_joined}){IGNORE_ARGS}){times_regex}"

    @staticmethod
    def get_times(pattern: PatternDict) -> TimesType:
        "Get `times` from pattern or None"

        return pattern.get('times', None)


    def _get_min_max_regex(self) -> Optional[str]:

        if self.times is None:
            return None

        if not isinstance(self.times, Dict):
            raise ValueError(f"times property inside {self.pattern} is not a Dict")

        min_amount = self.times.get('min', 1)
        max_amount = self.times.get('max', MAX_PYTHON_INT)

        if min_amount > max_amount:
            raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

        return f"{{{min_amount},{max_amount}}}"


    def _process_any(self, times_regex: Optional[str],
                          include_list: List[str],
                          exclude_list: List[str]
                          ) -> str:
        exclude_list_regex = join_instructions(inst_list=exclude_list, ignore_pattern=IGNORE_ARGS)
        include_list_regex = join_instructions(inst_list=include_list, ignore_pattern=IGNORE_ARGS)

        if times_regex is not None:
            return f"((?!{exclude_list_regex})({include_list_regex})){times_regex}"
        return f"((?!{exclude_list_regex})({include_list_regex}))"

    def _process_not(self, times_regex: Optional[str], exclude_list: List[str]) -> str:
        return self._generate_only_exclude(exclude_list_regex=exclude_list, times_regex=times_regex)

    def _process_simple(self, times_regex: Optional[str], include_list: List[str]) -> str:
        return self._generate_only_include(include_list_regex=include_list, times_regex=times_regex)

    def process(self) -> str:
        'Main process function for all patterns'
        times_regex_str: Optional[str] = self._get_min_max_regex()
        operand_regex = OperandsHandler(operands=self.operands).get_regex()

        if self.exclude_list is not None and self.include_list is not None:
            return self._process_any(times_regex=times_regex_str,
                                          include_list=self.include_list,
                                          exclude_list=self.exclude_list)
        if self.exclude_list is not None:
            return self._process_not(times_regex=times_regex_str,
                                          exclude_list=self.exclude_list)
        if self.include_list is not None:
            return self._process_simple(times_regex=times_regex_str,
                                             include_list=self.include_list)
        raise ValueError(
            f"Some error occurred. Include and exclude are empty for {self.pattern}")
