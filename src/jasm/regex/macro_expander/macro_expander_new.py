# pylint: disable=unused-import
from typing import Any, Dict, Generator, List, Optional, Tuple, TypeAlias, Union

MappingDict: TypeAlias = Dict
PatternTree: TypeAlias = Dict
MacroTree: TypeAlias = Dict


class MacroExpander:
    """Expand macros in a tree or pattern rule"""

    def resolve_all_macros(self, macros: Dict, tree: PatternTree) -> PatternTree:
        """Expand all macros in the tree in the order they are defined in the macros list"""
        tmp_tree = tree

        for macro in macros:
            tmp_tree = self.resolve_macro(macro=macro, tree=tmp_tree)
        return tmp_tree

    def resolve_macro(self, macro: Dict, tree: PatternTree) -> PatternTree:
        """Expand a macro in the tree"""

        if self.macro_has_args(macro=macro):
            macro = MacroArgsResolver().resolve(macro=macro, tree=tree)

        return self.apply_macro_recursively(macro=macro, tree=tree)

    def macro_has_args(self, macro: Dict) -> bool:
        """Check if a macro has arguments"""
        return "args" in macro

    def apply_macro_recursively(self, macro: Dict, tree: PatternTree) -> PatternTree:
        """Do the macro expansion in a tree recursively in order to allow modification of the tree while replacing"""

        # Check the current node of the tree for replacement
        if self.tree_should_be_expanded(tree=tree, macro=macro):
            tree = self.apply_macro_to_tree(node=tree, macro=macro)

        else:
            # Continue recursion on all children
            match tree:
                case dict():
                    for key, value in list(tree.items()):
                        match value:
                            case dict():
                                # Recursively apply to dictionaries and update the tree directly
                                tree[key] = self.apply_macro_recursively(macro=macro, tree=value)
                            case list():
                                # Apply to each element in the list and update the list directly
                                tree[key] = [self.apply_macro_recursively(tree=elem, macro=macro) for elem in value]

        return tree

    def tree_should_be_expanded(self, tree: PatternTree, macro: Dict) -> bool:
        """Check if the tree should be expanded"""
        return macro.get("name") in tree

    def apply_macro_to_tree(self, node: PatternTree, macro: Dict) -> PatternTree:
        """Apply the macro to the node"""
        assert macro.get("name") in node, f"Macro name {macro.get('name')} not found in the tree {node}"

        macro_pattern = macro.get("pattern")

        assert macro_pattern, f"Macro pattern {macro_pattern} not found in the macro {macro}"

        assert len(macro_pattern) == 1, f"Macro pattern {macro_pattern} must have only one key"

        return macro_pattern[0]

    def node_children(self, tree: PatternTree) -> Generator[PatternTree | List, None, None]:
        """Yield the children of a node in a tree"""
        for key, value in tree.items():
            if isinstance(value, (dict, list)):
                yield value


class MacroArgsResolver:

    def resolve(self, macro: Dict, tree: PatternTree) -> PatternTree:
        mapping_dict = self.get_macro_mapping_arg_dict(macro=macro, tree=tree)

        macro = self.evaluate_args_in_macro(macro=macro, mapping_dict=mapping_dict)

        return macro

    def get_macro_mapping_arg_dict(self, macro: Dict, tree: Dict) -> MappingDict:
        macro_args = macro.get("args")
        assert macro_args, "The macro must have args to replace."

        mapping_dict = ArgsMappingGenerator().get_args_mapping_dict(tree=tree, args=macro_args)
        return mapping_dict

    def evaluate_args_in_macro(self, macro: Dict, mapping_dict: MappingDict) -> PatternTree:
        """This function will replace the macro getting the args evaluation from the pattern"""

        macro_pattern = macro.get("pattern")

        for arg_key, arg_value in mapping_dict.items():
            for path, elem in self.iter_items_with_path(macro_pattern):
                match elem:
                    case str():
                        if arg_key == elem:
                            self.replace_item_in_structure(macro_pattern, path, arg_value)
                    case tuple():  # this tuple is the key-value pair of a dict
                        tree_key = elem[0]
                        tree_value = elem[1]
                        if arg_key == tree_key:
                            self.replace_item_in_structure(macro_pattern, path, arg_value)
                        if arg_key == tree_value:
                            self.replace_item_in_structure(macro_pattern, path, arg_value)

        macro["pattern"] = macro_pattern

        return macro

    def iter_items_with_path(
        self, elems: Union[str, List, Dict], path: Tuple = ()
    ) -> Generator[Tuple[Tuple, Any], None, None]:
        match elems:
            case str():
                yield path, elems
            case list():
                for i, elem in enumerate(elems):
                    yield from self.iter_items_with_path(elem, path + (i,))
            case dict():
                for k, v in elems.items():
                    yield path + (k,), (k, v)
                    yield from self.iter_items_with_path(v, path + (k,))

    def replace_item_in_structure(self, struct: Union[Dict, List], path: Tuple, new_value: Any) -> None:
        """Navigate struct using path and replace the target item with new_value."""
        for step in path[:-1]:
            struct = struct[step] if isinstance(struct, dict) else struct[int(step)]  # Navigate to the final container.
        if isinstance(struct, dict):
            struct[path[-1]] = new_value
        else:  # For lists, path[-1] is an index.
            struct[int(path[-1])] = new_value


class ArgsMappingGenerator:

    def get_args_mapping_dict(self, tree: Dict, args: List[str]) -> Dict:
        mapping_dict: Dict[str, Dict | List | str] = {}

        for arg in args:
            for item in self._get_args_mapping(tree=tree, current_arg=arg):
                mapping_dict.update(item)
        return mapping_dict

    def _get_args_mapping(self, tree: Dict, current_arg: str) -> Generator[Dict, None, None]:
        for key, value in self.yield_key_value_pairs(tree):
            if key == current_arg:
                yield {key: value}
        return None

    def yield_key_value_pairs(self, data: Union[Dict[Any, Any], List[Any]]) -> Generator[Tuple[Any, Any], None, None]:
        """
        Recursively yield key-value pairs from all levels of a nested structure
        containing dictionaries and lists.

        :param data: The nested structure to inspect.
        :yield: Key-value pairs from dictionaries at all nesting levels.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                yield key, value  # Yield the key-value pair of the dictionary
                if isinstance(value, (dict, list)):
                    # Recursively yield from nested dictionaries/lists
                    yield from self.yield_key_value_pairs(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    # Recursively yield from items if they are dictionaries/lists
                    yield from self.yield_key_value_pairs(item)
