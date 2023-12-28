"File2regex Yaml implementation module"

from typing import Any

import yaml

from src.global_definitions import Command
from src.logging_config import logger
from src.regex.directives_processors.tree_builder import (
    CommandBuilderNoParents,
    CommandParentsBuilder,
    CommandsTypeBuilder,
)
from src.regex.file2regex import File2Regex


class Yaml2Regex(File2Regex):
    "File2Regex class implementation with Yaml"

    def __init__(self, pattern_pathstr: str) -> None:
        self.loaded_file = self.load_file(file=pattern_pathstr)

    @staticmethod
    def load_file(file: str) -> Any:
        "Read a yaml file and return the parsed content"
        with open(file=file, mode="r", encoding="utf-8") as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.Loader)

    def produce_regex(self) -> str:
        "Handle all patterns and returns the final regex string"

        patterns = self.loaded_file.get("pattern", None)

        form_dict = {"$and": patterns}

        # Create rule tree
        rule_tree: Command = CommandBuilderNoParents(command_dict=form_dict).build()

        CommandParentsBuilder(rule_tree).build()
        CommandsTypeBuilder(rule_tree).build()

        # Process the rule tree and generate the regex

        output_regex = rule_tree.get_regex(rule_tree)

        # Log regex results
        logger.info("The output regex is:\n%s\n", output_regex)

        return output_regex
