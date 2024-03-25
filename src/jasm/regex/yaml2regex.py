"File2regex Yaml implementation module"

from typing import Any, Dict, List, Optional

import yaml

from jasm.global_definitions import DisassStyle, ValidAddrRange
from jasm.logging_config import logger
from jasm.regex.file2regex import File2Regex
from jasm.regex.macro_expander.macro_expander import MacroExpander, PatternTree
from jasm.regex.tree_generators.pattern_node import PatternNode, PatternNodeBase
from jasm.regex.tree_generators.pattern_node_builder import PatternNodeBuilderNoParents
from jasm.regex.tree_generators.pattern_node_parents_builder import PatternNodeParentsBuilder
from jasm.regex.tree_generators.pattern_node_type_builder import PatternNodeTypeBuilder


class Yaml2Regex(File2Regex):
    "File2Regex class implementation with Yaml"

    def __init__(self, pattern_pathstr: str, macros_from_terminal: Optional[List[str]] = None) -> None:
        self.loaded_file = self.load_file(file=pattern_pathstr)
        self.macros_from_terminal_filepath = macros_from_terminal

    @staticmethod
    def load_file(file: str) -> Any:
        "Read a yaml file and return the parsed content"
        with open(file=file, mode="r", encoding="utf-8") as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.Loader)

    def produce_regex(self) -> str:
        "Handle all patterns and returns the final regex string"

        patterns = self._get_pattern()

        rule_tree = self._generate_rule_tree(patterns=patterns)

        # Process the rule tree and generate the regex
        output_regex = rule_tree.get_regex()

        # Log regex results
        logger.debug("The output regex is:\n%s\n", output_regex)

        return output_regex

    def _get_pattern(self) -> PatternTree:
        # Load pattern
        patterns = self.loaded_file.get("pattern")

        pattern_with_top_node = {"$and": patterns}

        # Check if there are any macros setted
        macros: list = self.loaded_file.get("macros", [])

        assert isinstance(macros, list), "Invalid macros in the pattern file"

        if macros or self.macros_from_terminal_filepath:
            # Replace macros with their values

            if self.macros_from_terminal_filepath:
                # Add macros from args to the macros from the file
                processed_macros = self.load_macros_from_args()
                macros = processed_macros + macros

            pattern_with_top_node = MacroExpander().resolve_all_macros(macros=macros, tree=pattern_with_top_node)

        return pattern_with_top_node

    def load_macros_from_args(self) -> List[Dict]:
        "Load macros from a list of files"

        assert self.macros_from_terminal_filepath, "No macros from args provided"

        processed_macros = []
        for macro_file in self.macros_from_terminal_filepath:
            macro_file_content = self.load_file(file=macro_file)
            new_macro = macro_file_content.get("macros")
            processed_macros.extend(new_macro)

        return processed_macros

    def _generate_rule_tree(self, patterns: PatternTree) -> PatternNode:
        "Generate the rule tree from the patterns"
        # Generate the rule tree with no parents and type from root parent node downwards
        rule_tree: PatternNodeBase = PatternNodeBuilderNoParents(command_dict=patterns).build()

        # Transform parents of all nodes to commands
        PatternNodeParentsBuilder(rule_tree).build()

        # Add the command_type to each node
        rule_tree_complete = PatternNodeTypeBuilder(rule_tree, parent=None).build()

        return rule_tree_complete

    def get_assembly_style(self) -> DisassStyle:
        "Get the file style from the pattern file or return the default att"
        config = self.loaded_file.get("config")
        if config:
            style = config.get("style")
            match style:
                case "intel":
                    return DisassStyle.intel
                case "att":
                    return DisassStyle.att
                case _:
                    logger.error("Invalid or unsupported style: '%s' in the pattern file", style)

        return DisassStyle.att

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
