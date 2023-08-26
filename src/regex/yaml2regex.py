"File2regex Yaml implementation module"

from typing import Any, Dict
from abc import ABC, abstractmethod
import yaml

from src.logging_config import logger
from src.regex.any_directive_processor import AnyDirectiveProcessor
from src.regex.not_directive_processor import NotDirectiveProcessor
from src.regex.single_directive_processor import SingleDirectiveProcessor
from src.global_definitions import IGNORE_ARGS, Pattern, PathStr, PatternDict


class File2Regex(ABC):
    """Base class for file to regex converters"""

    @abstractmethod
    def load_file(self, file) -> Any:
        "Base method to load a file"

    @abstractmethod
    def produce_regex(self):
        "Main method to produce the regex"


class Yaml2Regex(File2Regex):
    "File2Regex class implementation with Yaml"

    def __init__(self, pattern_pathstr: PathStr) -> None:
        self.loaded_file = self.load_file(file=pattern_pathstr)

    @staticmethod
    def _read_yaml(file: PathStr) -> Any:
        "Read and return the parsed yaml"

        with open(file=file, mode="r", encoding="utf-8") as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.Loader)

    def load_file(self, file) -> Any:
        "Load file to Yaml2Regex"

        return self._read_yaml(file=file)

    @staticmethod
    def _process_dict_dispatcher(pattern: PatternDict) -> str:
        "Dispatch dict pattern. Resolve if pattern is $any, $not or $basic"

        dict_keys = pattern.keys()
        match list(dict_keys)[0]:
            case "$any":
                pattern: Dict[str, Any] = pattern["$any"]
                return AnyDirectiveProcessor(pattern).process()
            case "$not":
                pattern: Dict[str, Any] = pattern["$not"]
                return NotDirectiveProcessor(pattern).process()
            case _:
                return SingleDirectiveProcessor(pattern).process()

    def _handle_pattern(self, pattern: Pattern) -> str:
        "Dispatch pattern based on its type: str or dict"

        if isinstance(pattern, dict):
            return self._process_dict_dispatcher(pattern)
        if isinstance(pattern, str):
            return f"({pattern}{IGNORE_ARGS})"

        raise ValueError("Pattern type not valid")

    def produce_regex(self) -> str:
        "Handle all patterns and returns the final regex string"

        output_regex = ""
        for com in self.loaded_file["patterns"]:
            output_regex += self._handle_pattern(pattern=com)

        # Log regex results
        logger.info("The output regex is:\n %s\n", output_regex)

        return output_regex
