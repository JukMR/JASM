from typing import Any, Dict, Generator, List, Optional, Tuple, Union


class MacroExpander:
    """Expand macros in a pattern rule"""

    def resolve_macros(self, macros: dict, pattern: dict) -> dict:
        """Expand all macros in the pattern in the order they are defined in the macros list"""

        for macro in macros:
            tmp_pattern = self.replace_macro_in_pattern(macro=macro, pattern=pattern)

            assert isinstance(tmp_pattern, dict)
            pattern = tmp_pattern

        # The final `pattern` will always be a dict,
        # but because of the recursion `replace_macro_in_pattern` can return a list while iterating

        assert isinstance(
            pattern, dict
        ), f"The pattern must be a dict,\npattern_type: {type(pattern)}\npattern:{pattern}"
        return pattern

    def replace_macro_in_pattern(self, macro: dict, pattern: dict | List) -> dict | List | str:
        """Expand the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern.
        """
        match pattern:
            case dict():
                macro_args = macro.get("args")
                if macro_args:
                    for arg in macro_args:
                        if arg in pattern:
                            # Replace with argument
                            return self.replace_macro_in_pattern_dict(macro=macro, pattern=pattern, current_arg=arg)
                return self.replace_macro_in_pattern_dict(macro=macro, pattern=pattern)

            case list():
                return [self.replace_macro_in_pattern(macro=macro, pattern=elem) for elem in pattern]

            case str():
                if pattern == macro.get("name"):
                    macro_value = self.get_macro_pattern(macro=macro)
                    return macro_value

                if macro.get("name") in pattern:
                    # Doing string replacement only
                    assert isinstance(macro.get("pattern"), str)
                    new_name = pattern.replace(macro.get("name"), macro.get("pattern"))
                    return new_name
        return pattern

    def replace_macro_in_pattern_dict(self, macro: dict, pattern: dict, current_arg: Optional[str] = None) -> dict:
        """Expand the macro in the pattern when it is a dict"""

        macro_name = macro.get("name")
        for key, value in pattern.items():
            if key == macro_name:
                return self.replace_macro_in_pattern_dict_for_key(macro=macro, pattern=pattern, current_arg=current_arg)

            match value:
                case dict():
                    pattern[key] = self.replace_macro_in_pattern_dict(macro=macro, pattern=value)

                case list():
                    pattern[key] = [self.replace_macro_in_pattern(macro=macro, pattern=elem) for elem in value]

                case str():
                    if key == macro_name:
                        macro_value = self.get_macro_pattern(macro=macro)
                        pattern[key] = macro_value

                    elif macro_name in key:
                        # Doing string replacement only
                        tmp_value = pattern[key]
                        new_key_name = key.replace(macro_name, macro.get("pattern"))
                        pattern[new_key_name] = tmp_value
                        pattern.pop(key)

                    elif macro_name in value:
                        # Doing string replacement only
                        pattern[key] = value.replace(macro_name, macro.get("pattern"))

        return pattern

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

    def replace_macro_in_pattern_dict_for_key(
        self, macro: dict, pattern: dict, current_arg: Optional[str] = None
    ) -> dict:
        """Expand the macro in the pattern if it is a dict and the key matches the macro name"""

        macro_value = self.get_macro_pattern(macro=macro)

        assert isinstance(macro_value, dict)
        times = pattern.get("times")

        tmp_pattern = macro_value
        if times:
            tmp_pattern["times"] = times

        if current_arg:
            tmp_pattern = self.replace_arg_in_pattern(pattern=pattern, tmp_pattern=tmp_pattern, current_arg=current_arg)
        return tmp_pattern

    def replace_arg_in_pattern(self, pattern: Dict, tmp_pattern: Dict, current_arg: Optional[str] = None) -> Dict:
        assert current_arg, "current_arg must be provided."

        args_mapping = self.get_args_mapping(pattern, current_arg)
        assert args_mapping, "No mapping found for the current argument."

        def replace_item_in_structure(struct: Union[Dict, List], path: Tuple, new_value: Any):
            """Navigate struct using path and replace the target item with new_value."""
            for step in path[:-1]:
                struct = (
                    struct[step] if isinstance(struct, dict) else struct[int(step)]
                )  # Navigate to the final container.
            if isinstance(struct, dict):
                struct[path[-1]] = new_value
            else:  # For lists, path[-1] is an index.
                struct[int(path[-1])] = new_value

        for path, item in self.iter_items_with_path(tmp_pattern):
            if item == current_arg:
                replace_item_in_structure(tmp_pattern, path, args_mapping[current_arg])

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
                    yield from self.iter_items_with_path(v, path + (k,))
