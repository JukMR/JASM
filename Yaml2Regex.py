import yaml
from typing import Any, List, Dict, TypeAlias


from logging_config import logger


Command: TypeAlias = List[Any] | Dict[str, Any] | str

global IGNORE_ARGS
IGNORE_ARGS = r'[^\|]*\|'

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
        logger.debug(f"The output regex is: {output_regex}")

        return output_regex


class InstructionProcessor:

    def process_any(self, any_com: Command) -> str:
        if 'include_list' in any_com:
            output = ''
            for elem in any_com['include_list']:
                output += fr"{elem}{IGNORE_ARGS}|"
            output = '(' + output.rstrip(r'\|') + ')'

            min_amount = any_com['min']
            max_amount = any_com['max']

            if min_amount > max_amount:
                raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

            output += rf"{{{min_amount},{max_amount}}}"

            return output

        elif 'exclude_list' in any_com:
            output = ''
            for elem in any_com['exclude_list']:
                output += rf"{elem}{IGNORE_ARGS}|"
            output = '(' + output.rstrip(r'\|') + ')'

            min_amount = any_com['min']
            max_amount = any_com['max']

            if min_amount > max_amount:
                raise ValueError(f"Wrong min:{min_amount} or max:{max_amount} in yaml")

            exclude_output = rf"(?!.*{output})\|"

            # TODO: add this implementation
            # exclude_output += f"{{{min_amount},{max_amount}}}"

            return exclude_output

    def process_not(self, not_com: Command) -> str:
        not_command = not_com[0]
        return fr'(?!.*{not_command})\|'

    def process_mov(self, mov_com: Command) -> str:
        return r'mov[^\|]+\|'

    def process_dict(self, com) -> str:
        match list(com.keys())[0]:
            case '$any':
                return self.process_any(com['$any'])
            case '$not':
                return self.process_not(com['$not'])
            case 'mov':
                return self.process_mov(com['mov'])
            case _:
                raise ValueError('Invalid YAML input.')