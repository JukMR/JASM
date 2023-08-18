'Instruction Processor Module'
from dataclasses import dataclass
from typing import Any, List, Dict, Literal, Optional

from src.global_definitions import IGNORE_ARGS, MAX_PYTHON_INT
from src.global_definitions import PatternDict, IncludeListType, ExcludeListType, TimesType, OperandType


@dataclass
class InstructionProcessor:
    'Instruction Processor'
    pattern: PatternDict
    include_list: IncludeListType
    exclude_list: ExcludeListType
    times: TimesType
    operands: OperandType

    def _generate_only_include(self, include_list_regex: List[str], times_regex: Optional[str]) -> str:
        inst_joined = self._join_instructions(inst_list=include_list_regex)

        if times_regex is None:
            return f"({inst_joined})"

        return f"({inst_joined}){times_regex}"

    def _generate_only_exclude(self, exclude_list_regex: List[str], times_regex: Optional[str]) -> str:
        inst_joined = self._join_instructions(inst_list=exclude_list_regex)

        if times_regex is None:
            return f"((?!{inst_joined}){IGNORE_ARGS})"

        return f"((?!{inst_joined}){IGNORE_ARGS}){times_regex}"

    @staticmethod
    def _remove_last_character(string: str) -> str:
        return string[:-1]

    def _join_instructions(self, inst_list: List[str]) -> str:
        if len(inst_list) == 0:
            raise ValueError("There are no instructions to join")

        output = ''
        for elem in inst_list:
            output += f"{elem}{IGNORE_ARGS}|"

        output = self._remove_last_character(string=output)
        return output


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


    @staticmethod
    def get_times(pattern: PatternDict) -> TimesType:
        "Get `times` from pattern or None"
        return pattern.get('times', None)

    def process(self) -> str:
        'Main process function for all patterns'
        times_regex = self._get_min_max_regex()

        # $any case
        if self.exclude_list is not None and self.include_list is not None:

            exclude_list_regex = self._join_instructions(inst_list=self.exclude_list)
            include_list_regex = self._join_instructions(inst_list=self.include_list)

            if times_regex is not None:
                return f"((?!{exclude_list_regex})({include_list_regex})){times_regex}"

            return f"((?!{exclude_list_regex})({include_list_regex}))"

        # $not case
        if self.exclude_list is not None and self.include_list is None:
            return self._generate_only_exclude(exclude_list_regex=self.exclude_list,
                                               times_regex=times_regex)

        # Generic case
        if self.exclude_list is None and self.include_list is not None:
            return self._generate_only_include(include_list_regex=self.include_list,
                                               times_regex=times_regex)

        raise ValueError("Some error ocurred. "
                         + f"Both include and exclude are empty for {self.pattern}")


class BasicInstructionProcessor(InstructionProcessor):
    'Basic Instruction Processor'
    def __init__(self, basic_pattern: PatternDict) -> None:
        include_list = self._get_mnemonic_from_basic_pattern(pattern=basic_pattern)
        self._basic_properties = self._get_instruction_properties(include_list=include_list,
                                                            pattern=basic_pattern)

        super().__init__(pattern=basic_pattern, include_list=include_list,
                         exclude_list=None, times= super().get_times(basic_pattern),
                         operands=self._get_operands())

    @staticmethod
    def _get_mnemonic_from_basic_pattern(pattern: PatternDict) -> List[str]:
        reserved_patterns = ['operand', 'times']
        pattern_elems = [command for command in list(pattern.keys())
                         if command not in reserved_patterns]

        if len(pattern_elems) != 1:
            raise ValueError(f"Basic command {pattern_elems} has more than one instruction."
                             + "Should only be 1")

        return pattern_elems

    @staticmethod
    def _get_instruction_properties(include_list: IncludeListType,
                                    pattern: PatternDict) -> Dict[str, Any]:
        if include_list is None:
            raise ValueError(
                f"Some error happened and this basic instruction: {pattern}"
                + "doesn't have include_list")

        include_inst = include_list[0]

        instruction_properties = pattern[include_inst]
        if not isinstance(instruction_properties, Dict):
            raise ValueError(f"Returning properties {instruction_properties} is not a Dict")

        return instruction_properties


    def _get_operands(self) -> OperandType:
        return self._basic_properties.get('operands', None)


class NotInstructionProcessor(InstructionProcessor):
    '$not Instruction Processor'
    def __init__(self, not_pattern: PatternDict) -> None:
        exclude_list = not_pattern['inst']
        times = super().get_times(pattern=not_pattern)

        super().__init__(pattern=not_pattern, include_list=None, exclude_list=exclude_list,
                         times=times, operands=None)



class AnyInstructionProcessor(InstructionProcessor):
    '$any Instruction Processor'
    def __init__(self, any_pattern: PatternDict) -> None:
        include_list = self._get_instruction_list(pattern=any_pattern, pattern_type='include_list')
        exclude_list = self._get_instruction_list(pattern=any_pattern, pattern_type='exclude_list')
        times = super().get_times(pattern=any_pattern)

        super().__init__(pattern=any_pattern, include_list=include_list,
                         exclude_list=exclude_list, times=times, operands=None)

    @staticmethod
    def _get_instruction_list(pattern: PatternDict,
                              pattern_type: Literal['include_list', 'exclude_list']
                              ) -> Optional[List[str]]:
        if not isinstance(pattern, Dict):
            return None

        type_list = pattern.get(pattern_type, None)
        if not isinstance(type_list, Dict):
            return None

        type_list_inst = type_list.get('inst', None)
        if type_list_inst is None:
            return None

        if isinstance(type_list_inst, List):
            return type_list_inst
        raise ValueError(f"{type_list_inst} is not a List. It is: {type(type_list_inst)}")
