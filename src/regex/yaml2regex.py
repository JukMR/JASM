'yaml2regex module'

from typing import Any
import yaml

from src.logging_config import logger
from src.regex.instruction_processor import AnyInstructionProcessor, NotInstructionProcessor
from src.regex.instruction_processor import SingleInstructionProcessor
from src.global_definitions import IGNORE_ARGS, Pattern, PathStr, PatternDict


class Yaml2Regex:
    'Yaml2Regex class'
    def __init__(self, pattern_pathstr: PathStr) -> None:
        self.loaded_yaml = self.read_yaml(file=pattern_pathstr)

    @staticmethod
    def read_yaml(file: PathStr) -> Any:
        'Read and return the parsed yaml'
        with open(file=file, mode='r', encoding='utf-8') as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.Loader)


    @staticmethod
    def process_dict_pattern(pattern: PatternDict) -> str:
        'Dispatch dict pattern. Resolve if pattern is $any, $not or $basic'
        match list(pattern.keys())[0]:
            case '$any':
                pattern = pattern['$any']
                return AnyInstructionProcessor(pattern).process()
            case '$not':
                pattern = pattern['$not']
                return NotInstructionProcessor(pattern).process()
            case _:
                return SingleInstructionProcessor(pattern).process()


    def handle_pattern(self, pattern: Pattern) -> str:
        'Dispatch pattern based on its type: str or dict'

        if isinstance(pattern, dict):
            return self.process_dict_pattern(pattern)
        if isinstance(pattern, str):
            return f"({pattern}{IGNORE_ARGS})"

        raise ValueError("Pattern type not valid")


    def produce_regex(self) -> str:
        'Handle all patterns and returns the final string'
        output_regex = ''
        for com in self.loaded_yaml['patterns']:
            output_regex += self.handle_pattern(pattern=com)

        # Log results
        logger.info(msg=f"The output regex is:\n {output_regex}\n")

        return output_regex
