from typing import List, Optional

from jasm.global_definitions import DictNode, TimesType
from jasm.regex.tree_generators.pattern_node_abstract import PatternNodeData
from jasm.regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.regex.tree_generators.shared_context import SharedContext


class PatternNodeBuilderNoParents:
    def __init__(self, command_dict: DictNode, shared_context: SharedContext) -> None:
        self.command = command_dict
        self.shared_context = shared_context

        self.name: str | int
        self.times: TimesType
        self.children: Optional[List[PatternNodeTmpUntyped]]

        # Check if is instance of int or str
        match command_dict:
            case int() | str():
                self.name = command_dict
                self.times = TimesType(min_times=1, max_times=1)
                self.children = None

            case dict():
                self.name = self._get_name(command_dict)
                self.times = self._get_times(command_dict)
                self.children = self._get_children(name=self.name, command=command_dict, shared_context=shared_context)

            # Case when PatternNode is from a deref
            case tuple():
                self.name = command_dict[0]
                # self.time = self._get_times(command_dict) # TODO: Fix this
                self.times = TimesType(min_times=1, max_times=1)
                self.children = self._get_simple_child(name=command_dict[1], shared_context=shared_context)

            case _:
                raise ValueError(f"Command {command_dict} is not a valid type")

    @staticmethod
    def _get_name(command_dict: DictNode) -> str:
        assert isinstance(command_dict, dict)
        return list(command_dict.keys())[0]

    def _get_times(self, command_dict: DictNode) -> TimesType:
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
                    return TimesType(min_times=times, max_times=times)

                case dict():
                    min_time = times.get("min", 1)
                    max_time = times.get("max", 1)
                    return TimesType(min_times=min_time, max_times=max_time)

        return TimesType(min_times=1, max_times=1)

    @staticmethod
    def _get_children(name: str, command: DictNode, shared_context: SharedContext) -> List[PatternNodeTmpUntyped]:
        assert isinstance(command, dict)

        match command[name]:
            case list():
                return [
                    PatternNodeBuilderNoParents(command_dict=com, shared_context=shared_context).build()
                    for com in command[name]
                    if com != "times"
                ]
            case dict():
                return [
                    PatternNodeBuilderNoParents(command_dict=com, shared_context=shared_context).build()
                    for com in command[name].items()
                    if com != "times"
                ]

        raise ValueError("Command is not a list or a dict")

    @staticmethod
    def _get_simple_child(name: str, shared_context: SharedContext) -> List[PatternNodeTmpUntyped]:

        pattern_node_data = PatternNodeData(
            name=name,
            times=TimesType(min_times=1, max_times=1),
            children=None,
            parent=None,
            shared_context=shared_context,
        )

        return [PatternNodeTmpUntyped(pattern_node_data)]

    def build(self) -> PatternNodeTmpUntyped:
        assert isinstance(self.name, (str, int))

        pattern_node_data = PatternNodeData(
            name=self.name,
            times=self.times,
            children=self.children,
            parent=None,
            shared_context=self.shared_context,
        )

        return PatternNodeTmpUntyped(pattern_node_data)
