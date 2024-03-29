from typing import Any, Dict, Generator, List, Tuple, TypeAlias, Union

from jasm.regex.macro_expander.args_mapping_generator import ArgsMappingGenerator

# Type aliases
MappingDict: TypeAlias = Dict
PatternTree: TypeAlias = Dict | str
MacroTree: TypeAlias = Dict


class MacroArgsResolver:

    def resolve(self, macro: MacroTree, tree: PatternTree) -> MacroTree:
        mapping_dict = self._get_macro_mapping_arg_dict(macro=macro, tree=tree)

        macro = self._evaluate_args_in_macro(macro=macro, mapping_dict=mapping_dict)

        return macro

    def _get_macro_mapping_arg_dict(self, macro: MacroTree, tree: PatternTree) -> MappingDict:
        macro_args = macro.get("args")
        assert macro_args, "The macro must have args to replace."

        mapping_dict: MacroTree = ArgsMappingGenerator().get_args_mapping_dict(tree=tree, args=macro_args)
        return mapping_dict

    def _evaluate_args_in_macro(self, macro: MacroTree, mapping_dict: MappingDict) -> MacroTree:
        """This function will replace the macro getting the args evaluation from the pattern"""

        # This is done to ensure that the pattern is a dict or a list
        _tmp_macro_pattern = macro.get("pattern")
        assert isinstance(_tmp_macro_pattern, (dict, list))
        macro_pattern = _tmp_macro_pattern

        for arg_key, arg_value in mapping_dict.items():
            for path, elem in self._iter_items_with_path(macro_pattern):
                match elem:
                    case str():
                        if arg_key == elem:
                            self._replace_item_in_structure(macro_pattern, path, arg_value)
                    case tuple():  # this tuple is the key-value pair of a dict
                        tree_key = elem[0]
                        tree_value = elem[1]
                        if arg_key == tree_key:
                            self._replace_item_in_structure(macro_pattern, path, arg_value)
                        if arg_key == tree_value:
                            self._replace_item_in_structure(macro_pattern, path, arg_value)

        macro["pattern"] = macro_pattern

        return macro

    def _iter_items_with_path(
        self, elems: Union[str, List, Dict], path: Tuple = ()
    ) -> Generator[Tuple[Tuple, Any], None, None]:
        match elems:
            case str():
                yield path, elems
            case list():
                for i, elem in enumerate(elems):
                    yield from self._iter_items_with_path(elem, path + (i,))
            case dict():
                for k, v in elems.items():
                    yield path + (k,), (k, v)
                    yield from self._iter_items_with_path(v, path + (k,))

    def _replace_item_in_structure(self, struct: Union[Dict, List], path: Tuple, new_value: Any) -> None:
        """Navigate struct using path and replace the target item with new_value."""
        for step in path[:-1]:
            struct = struct[step] if isinstance(struct, dict) else struct[int(step)]  # Navigate to the final container.
        if isinstance(struct, dict):
            struct[path[-1]] = new_value
        else:  # For lists, path[-1] is an index.
            struct[int(path[-1])] = new_value
