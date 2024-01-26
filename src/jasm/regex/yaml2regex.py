"File2regex Yaml implementation module"

from typing import Any, Optional

import yaml

from jasm.global_definitions import EnumDisasStyle, ValidAddrRange
from jasm.logging_config import logger
from jasm.regex.command import PatternNode
from jasm.regex.file2regex import File2Regex
from jasm.regex.macro_expander import MacroExpander
from jasm.regex.tree_generators.tree_builder import (
    CommandBuilderNoParents,
    CommandParentsBuilder,
    CommandsTypeBuilder,
)


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

        patterns = self.get_pattern()

        rule_tree = self._generate_rule_tree(patterns=patterns)

        # Process the rule tree and generate the regex
        output_regex = rule_tree.get_regex(rule_tree)

        # Log regex results
        logger.info("The output regex is:\n%s\n", output_regex)

        return output_regex

    def get_pattern(self) -> dict:
        # Load pattern
        patterns = self.loaded_file.get("pattern")

        pattern_with_top_node = {"$and": patterns}

        # Check if there are any macros setted
        macros = self.loaded_file.get("macros")

        if macros:
            # Replace macros with their values
            return MacroExpander().resolve_macros(macros=macros, pattern=pattern_with_top_node)

        return pattern_with_top_node

    def _generate_rule_tree(self, patterns: dict) -> PatternNode:
        "Generate the rule tree from the patterns"
        # Generate the rule tree with no parents and type from root parent node downwards
        rule_tree: PatternNode = CommandBuilderNoParents(command_dict=patterns).build()

        # Transform parents of all nodes to commands
        CommandParentsBuilder(rule_tree).build()

        # Add the command_type to each node
        CommandsTypeBuilder(rule_tree).build()

        return rule_tree

    def get_assembly_style(self) -> Optional[EnumDisasStyle]:
        "Get the file style from the pattern file"
        config = self.loaded_file.get("config")
        if config:
            style = config.get("style")
        else:
            return None

        if style:
            if style == "intel":
                return EnumDisasStyle.intel
            if style == "att":
                return EnumDisasStyle.att
        return None

    def get_valid_addr_range(self) -> Optional[ValidAddrRange]:
        "Get the valid address range from the pattern file"
        config = self.loaded_file.get("config")
        if config:
            valid_addr = config.get("valid_addr_range")
        else:
            return None

        if valid_addr:
            return ValidAddrRange(min_addr=valid_addr.get("min"), max_addr=(valid_addr.get("max")))
        return None
