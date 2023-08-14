from dataclasses import dataclass
import sys
import yaml
from typing import Any, List, Dict, TypeAlias


from logging_config import logger


Pattern: TypeAlias = List[Any] | Dict[str, Any] | str

global IGNORE_ARGS
IGNORE_ARGS = r'[^\|]*\|'

global MAX_PYTHON_INT
MAX_PYTHON_INT = sys.maxsize * 2


class Yaml2Regex:
    def __init__(self, pattern_pathStr: str) -> None:
        self.loaded_yaml = self.read_yaml(file=pattern_pathStr)

    def read_yaml(self, file) -> Any:
        with open(file=file, mode='r', encoding='utf-8') as f:
            return yaml.load(stream=f.read(), Loader=yaml.Loader)

    def process_dict_pattern(self, pattern) -> str:
        match list(pattern.keys())[0]:
            case '$any':
                return AnyInstructionProcessor(pattern['$any']).process_any_pattern()
            case '$not':
                return NotInstructionProcessor(pattern['$not']).process_not_pattern()
            case _:
                return BasicInstructionProcessor(pattern).process()

    def handle_pattern(self, pattern: Pattern) -> str:

        if isinstance(pattern, dict):
            return self.process_dict_pattern(pattern)
        elif isinstance(pattern, str):
            return pattern + IGNORE_ARGS
        else:
            # TODO implementar excepcion para tipos no soportados por el programa
            raise ValueError("Pattern type not valid")

    def produce_regex(self):
        output_regex = ''
        for com in self.loaded_yaml['patterns']:
            output_regex += self.handle_pattern(pattern=com)

        # Log results
        logger.info(msg=f"The output regex is:\n {output_regex}")

        return output_regex


@dataclass
class Instruction:
    include_list: List[str] | None
    exclude_list: List[str] | None
    times: Dict | None
    operand: List[str] | None


class BasicInstructionProcessor(Instruction):
    def __init__(self, pattern: Dict) -> None:
        self.basic_pattern = pattern
        self.include_list = self._get_mnemonic_from_basic_pattern()
        self.exclude_list = None
        self._properties = self._get_Instruction_properties()
        self.times = self._get_times()
        self.operand = self._get_operands()

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

    def _get_operands(self) -> List[str] | None:
        self._properties.get('operands', None)

    def process(self) -> str:
        return AnyInstructionProcessor(self.basic_pattern,
                                    include_list=self.include_list,
                                    exclude_list=self.exclude_list,
                                    times=self.times).process_any_pattern()



class NotInstructionProcessor(Instruction):
    def __init__(self, not_pattern: Dict) -> None:
        self.not_pattern = not_pattern
        self.include_list = None
        self.exclude_list = self.not_pattern['inst']
        self.times = self._get_times()
        self.operand = None

    def _get_times(self) -> Dict | None:
        return self.not_pattern.get('times', None)

    def process_not_pattern(self) -> str:
        return AnyInstructionProcessor(self.not_pattern, include_list=self.include_list, exclude_list=self.exclude_list, times=self.times).process_any_pattern()


class AnyInstructionProcessor(Instruction):
    def __init__(self, any_pattern: Dict,
                 include_list: List[str] | None = None,
                 exclude_list: List[str] | None = None,
                 times: Dict | None = None,
                 ) -> None:
        self.any_pattern = any_pattern
        self.include_list = include_list or self.get_instruction_list(pattern=any_pattern, type='include_list')
        self.exclude_list = exclude_list or self.get_instruction_list(pattern=any_pattern, type='exclude_list')
        self.times = times or self._get_times()
        self.operand = None


    def _get_times(self) -> Any | None:
        return self.any_pattern.get('times', None)

    def get_min_max_regex(self) -> str | None:

        if self.times is None:
            return None

        if not isinstance(self.times, Dict):
            raise ValueError(f"times property inside {self.any_pattern} is not a Dict")

        min_amount = self.times.get('min', 1)
        max_amount = self.times.get('max', MAX_PYTHON_INT)

        if min_amount > max_amount:
            raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

        return f"{{{min_amount},{max_amount}}}"

    def get_instruction_list(self, pattern: Pattern, type: str) -> List[str] | None:
        if not isinstance(pattern, Dict):
            return None

        type_list = pattern.get(type, None)
        if not isinstance(type_list, Dict):
            return None

        type_list_inst = type_list.get('inst', None)
        if type_list_inst is None:
            return None

        return type_list_inst

    def _remove_last_character(self, string: str) -> str:
        return string[:-1]

    def join_instructions(self, inst_list: List[str]) -> str:
        if len(inst_list) == 0:
            raise ValueError("There are no instructions to join")

        output = ''
        for elem in inst_list:
            output += f"{elem}{IGNORE_ARGS}|"

        output = self._remove_last_character(string=output)
        return output

    def generate_only_include(self, include_list_regex: List[str], times_regex: str | None) -> str:
        inst_joined = self.join_instructions(inst_list=include_list_regex)

        if times_regex is None:
            return f"({inst_joined})"
        else:
            return f"({inst_joined}){times_regex}"

    def generate_only_exclude(self, exclude_list_regex: List[str], times_regex: str | None) -> str:
        inst_joined = self.join_instructions(inst_list=exclude_list_regex)

        if times_regex is None:
            return f"((?!{inst_joined}){IGNORE_ARGS})"
        else:
            return f"((?!{inst_joined}){IGNORE_ARGS}){times_regex}"

    def process_any_pattern(self) -> str:

            times_regex = self.get_min_max_regex()

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
                return self.generate_only_exclude(exclude_list_regex=self.exclude_list, times_regex=times_regex)

            # Generic case
            elif self.exclude_list is None and self.include_list is not None:
                return self.generate_only_include(include_list_regex=self.include_list, times_regex=times_regex)

            else:
                raise ValueError(f"Some error ocurred. Both include and exclude are empty for {self.any_pattern}")


