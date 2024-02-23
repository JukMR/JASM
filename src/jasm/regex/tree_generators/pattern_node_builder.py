from typing import List, Optional

from jasm.global_definitions import PatternNodeTypes, TimeType, dict_node
from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeBuilderNoParents:
    def __init__(self, command_dict: dict_node) -> None:
        self.command = command_dict

        # Check if is instance of int or str
        match self.command:
            case int() | str():
                self.name = self.command
                self.times = TimeType(min_times=1, max_times=1)
                self.children = None

            case dict():
                self.name = self._get_name(self.command)
                self.times = self._get_times(self.command)
                self.children = self._get_children(name=self.name, command=self.command)

            # Case when PatternNode is from a deref
            case tuple():
                self.name = self.command[0]
                # self.time = self._get_times(self.command) # TODO: Fix this
                self.times = TimeType(min_times=1, max_times=1)
                self.children = self.get_simple_child(self.command[1])

            case _:
                raise ValueError(f"Command {self.command} is not a valid type")

    @staticmethod
    def _get_name(command_dict: dict_node) -> str:
        assert isinstance(command_dict, dict)
        return list(command_dict.keys())[0]

    def _get_times(self, command_dict: dict_node) -> TimeType:
        assert isinstance(command_dict, dict)

        def _get_time_object(command_dict: dict) -> Optional[dict]:
            command_name = list(command_dict.keys())[0]

            # Command has no operands, only a time
            if "times" in command_dict.keys():
                return command_dict.get("times")

            # Command has operands and a time
            if "times" in command_dict[command_name]:
                return command_dict[command_name].get("times")
            return None

        if isinstance(command_dict, dict):
            times = _get_time_object(command_dict)

            match times:
                case int():
                    return TimeType(min_times=times, max_times=times)

                case dict():
                    min_time = times.get("min", 1)
                    max_time = times.get("max", 1)
                    return TimeType(min_times=min_time, max_times=max_time)

        return TimeType(min_times=1, max_times=1)

    @staticmethod
    def _get_children(name: str, command: dict_node) -> List[PatternNode]:
        assert isinstance(command, dict)

        match command[name]:
            case list():
                return [PatternNodeBuilderNoParents(com).build() for com in command[name] if com != "times"]
            case dict():
                return [PatternNodeBuilderNoParents(com).build() for com in command[name].items() if com != "times"]

        raise ValueError("Command is not a list or a dict")

    @staticmethod
    def get_simple_child(name: str) -> List[PatternNode]:
        return [
            PatternNode(
                name=name,
                times=TimeType(min_times=1, max_times=1),
                children=None,
                pattern_node_dict=name,
                pattern_node_type=PatternNodeTypes.deref_property,
                parent=None,
                root_node=None,
            )
        ]

    def build(self) -> PatternNode:
        assert isinstance(self.name, (str, int))

        return PatternNode(
            name=self.name,
            times=self.times,
            children=self.children,
            pattern_node_dict=self.command,
            pattern_node_type=None,
            parent=None,
            root_node=None,
        )
