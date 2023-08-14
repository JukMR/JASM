
from dataclasses import dataclass
from typing import Any, List, Dict

from global_definitions import Pattern, IGNORE_ARGS, MAX_PYTHON_INT


@dataclass
class InstructionProcessor:
    pattern: Pattern
    include_list: List[str] | None
    exclude_list: List[str] | None
    times: Dict | None
    operands: Dict | None

    def _generate_only_include(self, include_list_regex: List[str], times_regex: str | None) -> str:
        inst_joined = self.join_instructions(inst_list=include_list_regex)

        if times_regex is None:
            return f"({inst_joined})"
        else:
            return f"({inst_joined}){times_regex}"

    def _generate_only_exclude(self, exclude_list_regex: List[str], times_regex: str | None) -> str:
        inst_joined = self.join_instructions(inst_list=exclude_list_regex)

        if times_regex is None:
            return f"((?!{inst_joined}){IGNORE_ARGS})"
        else:
            return f"((?!{inst_joined}){IGNORE_ARGS}){times_regex}"

    @staticmethod
    def _remove_last_character(string: str) -> str:
        return string[:-1]

    def join_instructions(self, inst_list: List[str]) -> str:
        if len(inst_list) == 0:
            raise ValueError("There are no instructions to join")

        output = ''
        for elem in inst_list:
            output += f"{elem}{IGNORE_ARGS}|"

        output = self._remove_last_character(string=output)
        return output


    def _get_min_max_regex(self) -> str | None:

        if self.times is None:
            return None

        if not isinstance(self.times, Dict):
            raise ValueError(f"times property inside {self.pattern} is not a Dict")

        min_amount = self.times.get('min', 1)
        max_amount = self.times.get('max', MAX_PYTHON_INT)

        if min_amount > max_amount:
            raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

        return f"{{{min_amount},{max_amount}}}"


    def process(self) -> str:
        times_regex = self._get_min_max_regex()

        # $any case
        if self.exclude_list is not None and self.include_list is not None:

            exclude_list_regex = self.join_instructions(inst_list=self.exclude_list)
            include_list_regex = self.join_instructions(inst_list=self.include_list)

            if times_regex is not None:
                return f"((?!{exclude_list_regex})({include_list_regex})){times_regex}"
            else:
                return f"((?!{exclude_list_regex})({include_list_regex}))"

        # $not case
        elif self.exclude_list is not None and self.include_list is None:
            return self._generate_only_exclude(exclude_list_regex=self.exclude_list, times_regex=times_regex)

        # Generic case
        elif self.exclude_list is None and self.include_list is not None:
            return self._generate_only_include(include_list_regex=self.include_list, times_regex=times_regex)

        else:
            raise ValueError(f"Some error ocurred. Both include and exclude are empty for {self.pattern}")


class BasicInstructionProcessor(InstructionProcessor):
    def __init__(self, basic_pattern: Dict) -> None:
        self.basic_pattern = basic_pattern
        self.include_list = self._get_mnemonic_from_basic_pattern()
        self.exclude_list = None
        self._properties = self._get_Instruction_properties()
        self.times = self._get_times()
        self.operands = self._get_operands()

    def _get_mnemonic_from_basic_pattern(self) -> List[str]:
        reserved_patterns = ['operand', 'times']
        pattern_elems = [command for command in list(self.basic_pattern.keys()) if command not in reserved_patterns]

        if len(pattern_elems) != 1:
            raise ValueError(f"Basic command {pattern_elems} has more than one instruction. Should only be 1")

        return pattern_elems

    def _get_Instruction_properties(self) -> Dict:
        if self.include_list is None:
            raise ValueError(
                f"Some error happened and this basic instruction: {self.basic_pattern} doesn't have include_list")

        include_inst = self.include_list[0]
        return self.basic_pattern[include_inst]

    def _get_times(self) -> Dict | None:
        return self._properties.get('times', None)

    def _get_operands(self) -> Dict | None:
        return self._properties.get('operands', None)

    def process_basic_pattern(self) -> str:
        return InstructionProcessor(pattern=self.basic_pattern, include_list=self.include_list,
                            exclude_list=self.exclude_list, times=self.times,
                            operands=self.operands).process()


class NotInstructionProcessor(InstructionProcessor):
    def __init__(self, not_pattern: Dict) -> None:
        self.not_pattern = not_pattern
        self.include_list = None
        self.exclude_list = self.not_pattern['inst']
        self.times = self._get_times()
        self.operands = None

    def _get_times(self) -> Dict | None:
        return self.not_pattern.get('times', None)

    def process_not_pattern(self) -> str:
        return InstructionProcessor(pattern=self.not_pattern, include_list=self.include_list,
                                 exclude_list=self.exclude_list, times=self.times,
                                 operands=self.operands).process()


class AnyInstructionProcessor(InstructionProcessor):
    def __init__(self, any_pattern: Dict,
                 include_list: List[str] | None = None,
                 exclude_list: List[str] | None = None,
                 times: Dict | None = None,
                 ) -> None:

        self.any_pattern = any_pattern
        self.include_list = include_list or self._get_instruction_list(pattern=any_pattern, type='include_list')
        self.exclude_list = exclude_list or self._get_instruction_list(pattern=any_pattern, type='exclude_list')
        self.times = times or self._get_times()
        self.operands = None

    @staticmethod
    def _get_instruction_list(pattern: Pattern, type: str) -> List[str] | None:
        if not isinstance(pattern, Dict):
            return None

        type_list = pattern.get(type, None)
        if not isinstance(type_list, Dict):
            return None

        type_list_inst = type_list.get('inst', None)
        if type_list_inst is None:
            return None

        return type_list_inst

    def _get_times(self) -> Any | None:
        return self.any_pattern.get('times', None)


    def process_any_pattern(self) -> str:
        return InstructionProcessor(pattern=self.any_pattern, include_list=self.include_list,
                                 exclude_list=self.exclude_list, times=self.times,
                                 operands=self.operands).process()
