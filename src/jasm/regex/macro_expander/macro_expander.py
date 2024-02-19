from typing import Any, Dict, Generator, List, Optional, Tuple, Union


class MacroExpander:
    """Expand macros in a pattern rule"""

    def resolve_all_macros(self, macros: dict, tree: dict) -> dict:
        """Expand all macros in the pattern in the order they are defined in the macros list"""

        for macro in macros:
            tmp_tree = self.resolve_macro(macro=macro, tree=tree)

            assert isinstance(tmp_tree, dict)
            tree = tmp_tree

        # The final `pattern` will always be a dict,
        # but because of the recursion `replace_macro_in_pattern` can return a list while iterating

        assert isinstance(tree, dict), f"The tree must be a dict,\tree_type: {type(tree)}\ntree:{tree}"
        return tree

    def resolve_macro(self, macro: Dict, tree: Dict | List) -> Dict | List | str:
        """Expand the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern.
        """
        match tree:
            case dict():
                macro_args = macro.get("args")
                if macro_args:
                    # There are args to replace in the macro
                    macro = self.replace_args_in_macro(macro=macro, tree=tree)
                return self.replace_macro_in_tree_dict(macro=macro, tree=tree)

            case list():
                return [self.resolve_macro(macro=macro, tree=elem) for elem in tree]

            case str():
                if tree == macro.get("name"):
                    macro_value = self.get_macro_pattern(macro=macro)
                    return macro_value

                if macro.get("name") in tree:
                    # Doing string replacement only
                    assert isinstance(macro.get("pattern"), str)
                    new_name = tree.replace(macro.get("name"), macro.get("pattern"))
                    return new_name
        return tree

    def replace_args_in_macro(self, tree: Dict, macro: Dict) -> Dict:
        """This function will replace the macro getting the args evaluation from the pattern"""

        macro_args = macro.get("args")
        assert macro_args, "The macro must have args to replace."

        mapping_dict = ArgsMappingGenerator().get_args_mapping_dict(tree=tree, args=macro_args)

        if not mapping_dict:
            raise ValueError(f"No mapping found for the macro args: {macro_args}")

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

    def replace_macro_in_tree_dict(self, macro: dict, tree: dict) -> dict:
        """Expand the macro in the pattern when it is a dict"""

        macro_name = macro.get("name")
        for key, value in tree.items():
            match value:
                case dict():
                    if key == macro_name:
                        macro_pattern = macro.get("pattern")
                        assert len(macro_pattern) == 1
                        return macro_pattern[0]

                    tree[key] = self.replace_macro_in_tree_dict(macro=macro, tree=value)
                    return tree

                case list():
                    tree[key] = [self.resolve_macro(macro=macro, tree=elem) for elem in value]
                    return tree

                case str():
                    if key == macro_name:
                        macro_value = self.get_macro_pattern(macro=macro)
                        tree[key] = macro_value

                    elif macro_name in key:
                        # Doing string replacement only
                        tmp_value = tree[key]
                        new_key_name = key.replace(macro_name, macro.get("pattern"))
                        tree[new_key_name] = tmp_value
                        tree.pop(key)

                    elif macro_name in value:
                        # Doing string replacement only
                        tree[key] = value.replace(macro_name, macro.get("pattern"))

                    return tree

        raise ValueError("Invalid tree value: ")

    @staticmethod
    def get_macro_pattern(macro: dict) -> dict | str:
        """Return the macro pattern"""
        _macro_value_list = macro.get("pattern")

        if isinstance(_macro_value_list, str):
            # Macro value is only a string, doing string replacement only
            return _macro_value_list

        assert isinstance(_macro_value_list, List)
        macro_value = _macro_value_list[0]
        # Return a copy of the macro value so that the original macro is not modified

        match macro_value:
            case dict():
                return macro_value.copy()
            case str():
                # Macro value is a string, doing string replacement only
                return macro_value

        raise ValueError(f"Macro value must be a dict or a string, macro_value: {macro_value}")

    def replace_item_in_structure(self, struct: Union[Dict, List], path: Tuple, new_value: Any) -> None:
        """Navigate struct using path and replace the target item with new_value."""
        for step in path[:-1]:
            struct = struct[step] if isinstance(struct, dict) else struct[int(step)]  # Navigate to the final container.
        if isinstance(struct, dict):
            struct[path[-1]] = new_value
        else:  # For lists, path[-1] is an index.
            struct[int(path[-1])] = new_value

    def replace_arg_in_pattern(self, pattern: Dict, tmp_pattern: Dict, current_arg: Optional[str] = None) -> Dict:
        assert current_arg, "current_arg must be provided."

        args_mapping = self.get_args_mapping(pattern, current_arg)
        assert args_mapping, "No mapping found for the current argument."

        for path, item in self.iter_items_with_path(tmp_pattern):
            if item == current_arg:
                self.replace_item_in_structure(tmp_pattern, path, args_mapping[current_arg])

        return tmp_pattern

    def get_args_mapping(self, pattern: Dict, current_arg: str) -> Optional[Dict]:
        for k, v in pattern.items():
            if k == current_arg:
                return {k: v}
        return None

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


class ArgsMappingGenerator:

    def get_args_mapping_dict(self, tree: Dict, args: List[str]) -> Optional[Dict]:
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
