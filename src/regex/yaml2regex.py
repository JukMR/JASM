"File2regex Yaml implementation module"

from typing import Any, Dict
import yaml

from src.logging_config import logger
from src.global_definitions import SKIP_TO_END_OF_COMMAND, Pattern, PatternDict, IGNORE_INST_ADDR
from src.regex.file2regex import File2Regex
from src.regex.directives_processors.and_processor import AndDirectiveProcessor
from src.regex.directives_processors.not_processor import NotDirectiveProcessor
from src.regex.directives_processors.single_processor import SingleDirectiveProcessor
from src.regex.directive_processor import DirectiveProcessor


class Yaml2Regex(File2Regex):
    "File2Regex class implementation with Yaml"

    def __init__(self, pattern_pathstr: str) -> None:
        self.loaded_file = self.load_file(file=pattern_pathstr)

        # Get an empty DirectiveProcessor
        self.directive_processor = DirectiveProcessor(strategy=None)

    @staticmethod
    def load_file(file: str) -> Any:
        "Read a yaml file and return the parsed content"
        with open(file=file, mode="r", encoding="utf-8") as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.Loader)

    def _handle_pattern(self, pattern: Pattern) -> str:
        "Check if pattern is plain str or dict"

        if isinstance(pattern, dict):
            return self._process_dict(pattern)
        if isinstance(pattern, str):
            return f"({IGNORE_INST_ADDR}{pattern}{SKIP_TO_END_OF_COMMAND})"

        raise ValueError("Pattern type not valid")

    def _process_dict(self, pattern_arg: PatternDict) -> str:
        "Process dict pattern. Resolve if pattern is $and, $not or $basic"

        dict_keys = pattern_arg.keys()
        match list(dict_keys)[0]:
            case "$and":
                pattern: Dict[str, Any] = pattern_arg["$and"]
                self.directive_processor.set_strategy(AndDirectiveProcessor(pattern))
                return self.directive_processor.execute_strategy()
            case "$not":
                pattern: Dict[str, Any] = pattern_arg["$not"]
                self.directive_processor.set_strategy(NotDirectiveProcessor(pattern))
                return self.directive_processor.execute_strategy()
            case _:
                self.directive_processor.set_strategy(SingleDirectiveProcessor(pattern_arg))
                return self.directive_processor.execute_strategy()

    def produce_regex(self) -> str:
        "Handle all patterns and returns the final regex string"

        output_regex = ""
        for com in self.loaded_file["pattern"]:
            output_regex += self._handle_pattern(pattern=com)

        # Log regex results
        logger.info("The output regex is:\n%s\n", output_regex)

        return output_regex
