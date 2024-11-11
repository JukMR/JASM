import copy
from typing import Any, Dict, List, TypeAlias

from jasm.jasm_regex.macro_expander.macro_args_resolver import MacroArgsResolver

# Type aliases
PatternTree: TypeAlias = Dict[str, Any] | str
MacroTree: TypeAlias = Dict[str, Any]


class MacroExpander:
    """Expand macros in a tree or pattern rule"""

    @staticmethod
    def is_macro_name(identifier: str) -> bool:
        """Check if the given identifier starts with '@'"""
        return identifier.startswith("@")


    def resolve_all_macros(self, macros: List[MacroTree], pattern_tree: PatternTree) -> PatternTree:
        """Expand all macros in the tree in the order they are defined in the macros list"""
        if isinstance(pattern_tree, dict):
            tmp_tree = copy.deepcopy(pattern_tree)
        else:
            tmp_tree = pattern_tree

        # Ensure all macro names start with "@"
        for macro in macros:
            macro_name = macro.get("name")
            if not self.is_macro_name(macro_name):
                raise ValueError(f"Macro name {macro_name} must start with '@'")

        rule_macros = set()

        for macro in macros:
            tmp_tree = self._resolve_macro(macro=macro, tree=tmp_tree, rule_macros=rule_macros)

        # Ensure no unresolved macros remain
        if rule_macros:
            raise ValueError(f"The following macros are not defined: {rule_macros}")

        return tmp_tree

    def _resolve_macro(self, macro: MacroTree, tree: PatternTree, rule_macros: set) -> PatternTree:
        """Expand a macro in the tree"""
        return self._apply_macro_recursively(macro=macro, tree=tree, rule_macros=rule_macros)

    def _macro_has_args(self, macro: MacroTree) -> bool:
        """Check if a macro has arguments"""
        return "args" in macro

    def _apply_macro_recursively(
        self, macro: MacroTree, tree: PatternTree, rule_macros: set
    ) -> PatternTree:
        """Do the macro expansion in a tree recursively in order to allow modification of the tree while replacing"""

        macro_name = macro.get("name")
        assert isinstance(macro_name, str), f"Macro name {macro_name} is not a string"

        match tree:
        # String replacement macro mode
            case str():
                if self.is_macro_name(tree):
                    rule_macros.add(tree)
                return self._process_str_tree(
                    tree=tree, macro_name=macro_name, macro=macro, rule_macros=rule_macros
                )

            # Subtree replacement macro mode
            case dict():
                return self._process_dict_tree(
                    tree=tree, macro_name=macro_name, macro=macro, rule_macros=rule_macros
                )

            # Just in case, should never happen
            case _:
                return tree

    def _process_str_tree(
        self, tree: str, macro_name: str, macro: MacroTree, rule_macros: set
    ) -> PatternTree:
        """
        Process the tree when it is a string.
        This is the case when the macro is just a string substitution.
        """

        # Case of full string matching
        if macro_name == tree:
            rule_macros.discard(tree)
            return self._apply_macro_to_tree(node=tree, macro=macro)

        # Case of substring matching
        if macro_name in tree:
            rule_macros.discard(tree)
            return self._apply_macro_to_tree_substring(node=tree, macro=macro)

        return tree

    def _process_dict_tree(
        self, tree: Dict[str, Any], macro_name: str, macro: MacroTree, rule_macros: set
    ) -> PatternTree:
        """
        Process the tree when it is a dictionary.
        This is the case when the macro is a subtree replacement.
        """

        if macro_name in tree:
            rule_macros.discard(macro_name)
            return self._apply_macro_to_tree(node=tree, macro=macro)

        # Continue recursion on all children
        for key, value in list(tree.items()):
            match value:
                case dict():
                    # Recursively apply to dictionaries and update the tree directly
                    tree[key] = self._apply_macro_recursively(
                        macro=macro, tree=value, rule_macros=rule_macros
                    )
                case list():
                    # Apply to each element in the list and update the list directly
                    tree[key] = [
                        self._apply_macro_recursively(
                            tree=elem, macro=macro, rule_macros=rule_macros
                        ) for elem in value
                    ]
                case str():
                    # Case where the macro is just string substitution but on values
                    if self.is_macro_name(value):
                        rule_macros.add(value)
                    tree[key] = self._process_str_tree(
                        tree=value, macro_name=macro_name, macro=macro, rule_macros=rule_macros
                    )
        return tree

    def _resolve_local_macro(self, node: PatternTree, macro: MacroTree) -> MacroTree:
        """Copy the macro and resolve its arguments"""
        macro_copy = macro
        if self._macro_has_args(macro=macro):
            macro_copy = copy.deepcopy(macro)
            macro_copy = MacroArgsResolver().resolve(macro=macro_copy, tree=node)
        return macro_copy

    def _apply_macro_to_tree(self, node: PatternTree, macro: MacroTree) -> PatternTree:
        """Apply the macro to the node"""

        local_macro = self._resolve_local_macro(node=node, macro=macro)
        macro_pattern = local_macro.get("pattern")
        assert macro_pattern, f"Macro pattern {macro_pattern} not found in the macro {local_macro}"

        macro_name: str = local_macro.get("name")
        assert isinstance(macro_name, str), f"Macro name {macro_name} is not a string"

        match node:
            case str():
                # Case of full string matching or case of substring matching
                assert macro_name and (
                    macro_name == node or macro_name in node
                ), f"Node {node} is not equal to the macro name nor is substring {macro_name}"

            case dict():
                assert macro_name in node, f"Macro name {macro_name} not found in the tree {node}"

        match macro_pattern:
            case str():
                # Return the macro replaced with its times
                if isinstance(node, dict):
                    times: dict = node[macro_name]
                    assert isinstance(times, dict), f"Times {times} must be a dictionary"

                    assert "times" in times
                    return {macro_pattern: times}

                return macro_pattern

            case list():
                assert len(
                    macro_pattern
                ) == 1, f"Macro pattern {macro_pattern} must have only one key"
                return macro_pattern[0]  # type: ignore

        raise ValueError(f"Macro pattern {macro_pattern} is not a valid type")

    def _apply_macro_to_tree_substring(self, node: str, macro: MacroTree) -> str:
        local_macro = self._resolve_local_macro(node=node, macro=macro)
        macro_pattern = local_macro.get("pattern")
        assert macro_pattern, f"Macro pattern {macro_pattern} not found in the macro {local_macro}"

        macro_name, macro_pattern = local_macro.get("name"), local_macro.get("pattern")
        assert (
            macro_name and macro_pattern
        ), f"Macro name {macro_name} and pattern {macro_pattern} not found in the macro"

        return node.replace(macro_name, macro_pattern)
