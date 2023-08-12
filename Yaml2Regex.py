import yaml
from typing import Any, List, Dict, TypeAlias


from logging_config import logger


Command: TypeAlias = List[Any] | Dict[str, Any] | str

global IGNORE_ARGS
IGNORE_ARGS = r'[^\|]*\|'

import sys
global MAX_PYTHON_INT
MAX_PYTHON_INT = sys.maxsize * 2

class Yaml2Regex:
    def __init__(self, yaml_pathStr: str) -> None:
        self.loaded_yaml = self.read_yaml(yaml_pathStr)
        self.processor = InstructionProcessor()

    def read_yaml(self, file) -> Any:
        with open(file, 'r', encoding='utf-8') as f:
            return yaml.load(stream=f.read(), Loader=yaml.Loader)

    def handle_yaml_command(self, com: Command) -> str:

        if isinstance(com, dict):
            return self.processor.process_dict(com)
        elif isinstance(com, str):
            return com + IGNORE_ARGS
        else:
            # TODO implementar excepcion para tipos no soportados por el programa
            raise ValueError("Command type not valid")


    def produce_regex(self):
        output_regex = ''
        for com in self.loaded_yaml['commands']:
            output_regex += self.handle_yaml_command(com)

        # Log results
        logger.debug(f"The output regex is:\n {output_regex}")

        return output_regex


class InstructionProcessor:

    def _remove_last_character(self, string: str) -> str:
        return string[:-1]

    def join_instructions(self, list_inst: List[str]) -> str:
        if len(list_inst) == 0:
            raise ValueError("There are no instructions to join")

        output = ''
        for elem in list_inst:
            output += f"{elem}{IGNORE_ARGS}|"

        return self._remove_last_character(output)

    def generate_only_include(self, include_list_regex: List[str], times_regex: str | None) -> str:
        output = self.join_instructions(include_list_regex)

        if times_regex is None:
            return f"({output}{IGNORE_ARGS})"
        else:
            return f"({output}{IGNORE_ARGS}){times_regex}"

    def generate_only_exclude(self, exclude_list_regex: List[str], times_regex: str | None) -> str:
        output = self.join_instructions(exclude_list_regex)

        if times_regex is None:
            return f"((?!.*{output}){IGNORE_ARGS})"
        else:
            return f"((?!.*{output}){IGNORE_ARGS}){times_regex}"


    def get_instruction_list(self, com: Command, type: str) -> List[str] | None:
        if not isinstance(com, Dict):
            return None

        type_list = com.get(type, None)
        if not isinstance(type_list, Dict):
            return None

        type_list_inst = type_list.get('inst', None)
        if type_list_inst is None:
            return None

        return type_list_inst


    def process_any(self, any_com: Command,
                    include_list_inst: List[str] | None = None,
                    exclude_inst_list: List[str] | None = None
                    ) -> str:


        times_regex = self.get_min_max_regex(any_com)

        include_list = self.get_instruction_list(com=any_com, type='include_list') or include_list_inst
        exclude_list = self.get_instruction_list(com=any_com, type='exclude_list') or exclude_inst_list

        # $any case
        if exclude_list is not None and include_list is not None:

            exclude_list_regex = self.join_instructions(exclude_list)
            include_list_regex = self.join_instructions(include_list)

            return f"((?!.*{exclude_list_regex})({include_list_regex})){times_regex}"

        # $not case
        elif exclude_list is not None and include_list is None:
            return self.generate_only_exclude(exclude_list_regex=exclude_list, times_regex=times_regex)


        # Generic case
        elif exclude_list is None and include_list is not None:
            return self.generate_only_include(include_list_regex=include_list, times_regex=times_regex)

        else:
            raise ValueError(f"Some error ocurred. Both include and exclude are empty for {any_com}")


    def get_min_max_regex(self, any_com: Command) -> str | None:
        if not isinstance(any_com, Dict):
            return None

        times_pattern = any_com.get('times', None)

        if not isinstance(times_pattern, Dict):
            raise ValueError(f"times property inside {any_com} is not a Dict")

        min_amount = times_pattern.get('min', 0)
        max_amount = times_pattern.get('max', MAX_PYTHON_INT)

        if min_amount > max_amount:
            raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

        return f"{{{min_amount},{max_amount}}}"


    def process_not(self, not_com: str) -> str:
        not_command = [not_com[0]]

        return self.process_any(not_com, exclude_inst_list=not_command)


    def process_generic_command(self, generic_com: str) -> str:
        generic_command = [generic_com[0]]
        return self.process_any(generic_com, include_list_inst=generic_command)

    def process_dict(self, com) -> str:
        match list(com.keys())[0]:
            case '$any':
                return self.process_any(com['$any'])
            case '$not':
                return self.process_not(com['$not'])
            case _:
                return self.process_generic_command(com)