"File2regex Yaml implementation module"

from typing import Any, List

import yaml

from src.command_definition import Command
from src.logging_config import logger
from src.regex.tree_generators.tree_builder import (
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

    def _generate_rule_tree(self, patterns: List[str]) -> Command:
        "Generate the rule tree from the patterns"
        form_dict = {"$and": patterns}

        # Generate the rule tree with no parents and type from root parent node downwards
        rule_tree: Command = CommandBuilderNoParents(command_dict=form_dict).build()

        # Transform parents of all nodes to commands
        CommandParentsBuilder(rule_tree).build()

        # Add the command_type to each node
        CommandsTypeBuilder(rule_tree).build()

        return rule_tree

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

        # Check if there are any macros setted
        macros = self.loaded_file.get("macros")

        if macros:
            # Replace macros with their values
            return MacroReplacer().resolve_macros(macros=macros, pattern=patterns)

        return patterns


class MacroReplacer:
    def resolve_macros(self, macros: dict, pattern: dict | list) -> dict | list:
        for macro in macros:
            pattern = self.replace_macro_in_pattern(macro=macro, pattern=pattern)

        return pattern

    def replace_macro_in_pattern(self, macro: dict, pattern: dict | list) -> dict | list:
        """Replace the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern using a BFS approach.
        """
        if isinstance(pattern, dict):
            return self.replace_macro_in_pattern_dict(macro=macro, pattern=pattern)
        if isinstance(pattern, list):
            return self.replace_macro_in_pattern_in_list(macro=macro, pattern=pattern)

        if isinstance(pattern, str):
            if pattern == macro.get("name"):
                macro_pattern = macro.get("pattern")[0]
                return macro_pattern
        return pattern

    def replace_macro_in_pattern_dict(self, macro: dict, pattern: dict) -> dict:
        """Replace the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern using a BFS approach.
        """

        # Replace the macro in the pattern
        macro_name = macro.get("name")
        for key, value in pattern.items():
            if key == macro_name:
                pattern = self.replace_macro_in_pattern_dict_for_key(macro=macro, pattern=pattern)
                continue

            if isinstance(value, dict):
                pattern[key] = self.replace_macro_in_pattern_dict(macro=macro, pattern=value)
                continue

            if isinstance(value, list):
                pattern[key] = self.replace_macro_in_pattern_in_list(macro=macro, pattern=value)
                continue

            if isinstance(value, str):
                if key == macro_name:
                    macro_value = macro.get("pattern")[0]
                    pattern[key] = macro_value
                    continue

        return pattern

    @staticmethod
    def replace_macro_in_pattern_dict_for_key(macro: dict, pattern: dict) -> dict:
        macro_value_list = macro.get("pattern")
        assert isinstance(macro_value_list, list)
        macro_value = macro_value_list[0]
        # Replace pattern with macro value

        times = pattern.get("times")
        pattern = macro_value
        if times:
            pattern["times"] = times
        return pattern

    def replace_macro_in_pattern_in_list(self, macro: dict, pattern: list) -> list:
        """Replace the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern using a BFS approach.
        """
        # Replace the macro in the pattern
        return [self.replace_macro_in_pattern(macro=macro, pattern=elem) for elem in pattern]
