from typing import List


class MacroExpander:
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

    def replace_macro_in_pattern(self, macro: dict, pattern: dict | List) -> dict | List:
        """Expand the macro in the pattern

        This algoritm will replace all the occurrences of the macro in the pattern.
        """
        if isinstance(pattern, dict):
            return self.replace_macro_in_pattern_dict(macro=macro, pattern=pattern)
        if isinstance(pattern, List):
            return self.replace_macro_in_pattern_in_list(macro=macro, pattern=pattern)

        if isinstance(pattern, str):
            if pattern == macro.get("name"):
                macro_value = self.get_macro_pattern(macro=macro)
                return macro_value
        return pattern

    def replace_macro_in_pattern_dict(self, macro: dict, pattern: dict) -> dict:
        """Expand the macro in the pattern when it is a dict"""

        macro_name = macro.get("name")
        for key, value in pattern.items():
            if key == macro_name:
                return self.replace_macro_in_pattern_dict_for_key(macro=macro, pattern=pattern)

            if isinstance(value, dict):
                pattern[key] = self.replace_macro_in_pattern_dict(macro=macro, pattern=value)
                continue

            if isinstance(value, List):
                pattern[key] = self.replace_macro_in_pattern_in_list(macro=macro, pattern=value)
                continue

            if isinstance(value, str):
                if key == macro_name:
                    macro_value = self.get_macro_pattern(macro=macro)
                    pattern[key] = macro_value
                    continue

        return pattern

    @staticmethod
    def get_macro_pattern(macro: dict) -> dict:
        """Return the macro pattern"""
        _macro_value_list = macro.get("pattern")
        assert isinstance(_macro_value_list, List)
        macro_value = _macro_value_list[0]
        # Return a copy of the macro value so that the original macro is not modified

        assert isinstance(macro_value, dict)
        return macro_value.copy()

    def replace_macro_in_pattern_dict_for_key(self, macro: dict, pattern: dict) -> dict:
        """Expand the macro in the pattern if it is a dict and the key matches the macro name"""
        macro_value = self.get_macro_pattern(macro=macro)

        assert isinstance(macro_value, dict)
        times = pattern.get("times")

        tmp_pattern = macro_value
        if times:
            tmp_pattern["times"] = times
        return tmp_pattern

    def replace_macro_in_pattern_in_list(self, macro: dict, pattern: List) -> List:
        """Replace the macro in the pattern when the pattern is a list"""
        return [self.replace_macro_in_pattern(macro=macro, pattern=elem) for elem in pattern]
