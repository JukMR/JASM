import yaml
from typing import Any


from logging_config import logger
from InstructionProcessor import AnyInstructionProcessor, NotInstructionProcessor, BasicInstructionProcessor
from global_definitions import IGNORE_ARGS, Pattern


class Yaml2Regex:
    def __init__(self, pattern_pathStr: str) -> None:
        self.loaded_yaml = self.read_yaml(file=pattern_pathStr)

    @staticmethod
    def read_yaml(file) -> Any:
        with open(file=file, mode='r', encoding='utf-8') as f:
            return yaml.load(stream=f.read(), Loader=yaml.Loader)

    @staticmethod
    def process_dict_pattern(pattern) -> str:
        match list(pattern.keys())[0]:
            case '$any':
                pattern = pattern['$any']
                return AnyInstructionProcessor(pattern).process_any_pattern()
            case '$not':
                pattern = pattern['$not']
                return NotInstructionProcessor(pattern).process_not_pattern()
            case _:
                return BasicInstructionProcessor(pattern).process_basic_pattern()

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