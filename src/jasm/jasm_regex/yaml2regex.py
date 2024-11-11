from typing import Any, Dict, List, Optional
import yaml
from jasm.global_definitions import JASMConfig
from jasm.logging_config import logger
from jasm.jasm_regex.file2regex import File2Regex
from jasm.jasm_regex.macro_expander.macro_expander import MacroExpander, PatternTree
from jasm.jasm_regex.tree_generators.capture_manager import CapturesManager
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.jasm_regex.tree_generators.pattern_node_builder import PatternNodeBuilderNoParents
from jasm.jasm_regex.tree_generators.pattern_node_type_builder.ast_builder import GeneralPatternNodeBuilder
from jasm.jasm_regex.tree_generators.shared_context import SharedContext


class Yaml2Regex(File2Regex):  # type: ignore
    """File2Regex class implementation with Yaml"""

    def __init__(
        self, pattern_pathstr: str, macros_from_terminal: Optional[List[str]] = None
    ) -> None:
        self.loaded_file = self.load_file(file=pattern_pathstr)
        self.macros_from_terminal_filepath = macros_from_terminal
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration into the singleton from the loaded file."""
        config = self.loaded_file.get("config", {})
        JASMConfig.get_instance().load_config(config)

    @staticmethod
    def load_file(file: str) -> Any:
        """Read a yaml file and return the parsed content"""
        with open(file=file, mode="r", encoding="utf-8") as file_descriptor:
            return yaml.load(stream=file_descriptor.read(), Loader=yaml.SafeLoader)

    def produce_regex(self) -> str:
        """Handle all patterns and returns the final regex string"""

        patterns = self._get_pattern()

        rule_tree = self._generate_rule_tree(patterns=patterns)

        # Process the rule tree and generate the regex
        output_regex: str = rule_tree.get_regex()

        # Log regex results
        logger.debug("The output regex is:\n%s\n", output_regex)

        return output_regex

    def _get_pattern(self) -> PatternTree:
        """Load pattern from file"""
        patterns = self.loaded_file.get("pattern")

        pattern_with_top_node = {"$and": patterns}

        # Check if there are any macros set
        macros: list[dict[str, str]] = self.loaded_file.get("macros", [])

        if not isinstance(macros, list):
            raise ValueError("Invalid macros in the pattern file")

        if macros or self.macros_from_terminal_filepath:
            # Replace macros with their values

            if self.macros_from_terminal_filepath:
                # Add macros from args to the macros from the file
                processed_macros: list[dict[str, str]] = self.load_macros_from_args()
                macros = processed_macros + macros

            pattern_with_top_node = MacroExpander().resolve_all_macros(
                macros=macros, pattern_tree=pattern_with_top_node
            )

        return pattern_with_top_node

    def load_macros_from_args(self) -> List[Dict[str, str]]:
        """Load macros from a list of files"""

        if not self.macros_from_terminal_filepath:
            raise ValueError("No macros from args provided")

        processed_macros = []
        for macro_file in self.macros_from_terminal_filepath:
            macro_file_content = self.load_file(file=macro_file)
            new_macro = macro_file_content.get("macros")
            processed_macros.extend(new_macro)

        return processed_macros

    def context_initializer(self) -> SharedContext:
        """Initialize shared_context with empty capture group references"""

        shared_context = SharedContext(capture_manager=CapturesManager())
        return shared_context

    def _generate_rule_tree(self, patterns: PatternTree) -> PatternNode:
        """Generate the rule tree from the patterns"""

        shared_context = self.context_initializer()

        # Generate the rule tree with no parents and all nodes untyped (PatternNodeTmpUntyped)
        rule_tree: PatternNode = PatternNodeBuilderNoParents(
            command_dict=patterns, shared_context=shared_context
        ).build()

        # Transform each node in the rule tree to a typed node
        return GeneralPatternNodeBuilder().build(rule_tree)
