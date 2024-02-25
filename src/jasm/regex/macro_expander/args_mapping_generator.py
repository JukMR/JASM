from typing import Any, Dict, Generator, List, Tuple, TypeAlias, Union


# Type aliases
PatternTree: TypeAlias = Dict | str


class ArgsMappingGenerator:

    def get_args_mapping_dict(self, tree: PatternTree, args: List[str]) -> Dict:
        mapping_dict: Dict[str, Dict | List | str] = {}

        for arg in args:
            for item in self._get_args_mapping(tree=tree, current_arg=arg):
                mapping_dict.update(item)
        return mapping_dict

    def _get_args_mapping(self, tree: PatternTree, current_arg: str) -> Generator[Dict, None, None]:
        match tree:
            case str():
                if tree == current_arg:
                    yield {current_arg: tree}

            case dict():
                for key, value in self.yield_key_value_pairs(tree):
                    if key == current_arg:
                        yield {key: value}

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
