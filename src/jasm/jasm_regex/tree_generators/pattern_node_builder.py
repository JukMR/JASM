from typing import Any, Dict, List, Optional, TypeAlias

from jasm.global_definitions import DictNode, TimesType
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNodeData
from jasm.jasm_regex.tree_generators.pattern_node_tmp_untyped import PatternNodeTmpUntyped
from jasm.jasm_regex.tree_generators.shared_context import SharedContext

CommandDict: TypeAlias = dict[str, list[str] | dict[str, str | int]]


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
                self._handle_simple_case(command_dict, shared_context)
            case dict():
                self._handle_dict_case(command_dict, shared_context)

            # Case when PatternNode is from a deref
            case tuple():
                self._handle_tuple_case(command_dict, shared_context)

            case _:
                raise ValueError(f"Command {command_dict} is not a valid type")

    def _handle_simple_case(self, command_dict: int | str, shared_context: SharedContext) -> None:
        self.name = command_dict
        self.times = TimesType(_min_times=1, _max_times=1)
        self.children = None

    def _handle_dict_case(self, command_dict: dict, shared_context: SharedContext) -> None:
        self.name = self._get_name(command_dict)
        self.times = self._get_times(command_dict)
        self.children = self._get_children(
            name=self.name, command=command_dict, shared_context=shared_context
        )

    def _handle_tuple_case(self, command_dict: tuple, shared_context: SharedContext) -> None:
        self.name = command_dict[0]
        self.times = TimesType(_min_times=1, _max_times=1)
        command_son = command_dict[1]
        match command_son:
            case list():
                self.children = [
                    PatternNodeBuilderNoParents(command_dict=elem,
                                                shared_context=shared_context).build()
                    for elem in command_son
                ]
            case _:
                self.children = self._get_simple_child(
                    name=command_dict[1], shared_context=shared_context
                )

    @staticmethod
    def _get_name(command_dict: DictNode) -> str:
        assert isinstance(command_dict, dict)
        name_key: str = list(command_dict.keys())[0]
        return name_key

    @staticmethod
    def _get_times(command_dict: DictNode) -> TimesType:
        assert isinstance(command_dict, dict)

        def _get_time_object(
            command_dict: Dict[str, Dict[str, int]]
        ) -> Optional[dict[str, Any] | int]:
            command_name = list(command_dict.keys())[0]

            # Command has no operands, only a time
            if "times" in command_dict.keys():
                return command_dict.get("times")

            # Command has operands and a time
            if "times" in command_dict[command_name]:
                assert isinstance(command_dict[command_name], dict)

                command_dict_name: dict[str, int] = command_dict[command_name]

                times = command_dict_name.get("times")
                assert isinstance(times, (int, dict))

                return times
            return None

        if isinstance(command_dict, dict):
            times = _get_time_object(command_dict)

            match times:
                case int():
                    return TimesType(_min_times=times, _max_times=times)

                case dict():
                    min_time = times.get("min", 1)
                    max_time = times.get("max", 1)
                    return TimesType(_min_times=min_time, _max_times=max_time)

        return TimesType(_min_times=1, _max_times=1)

    @staticmethod
    def _get_children(name: str, command: DictNode,
                      shared_context: SharedContext) -> List[PatternNodeTmpUntyped]:
        assert isinstance(command, dict)

        match command[name]:
            case list():
                return [
                    PatternNodeBuilderNoParents(command_dict=com,
                                                shared_context=shared_context).build()
                    for com in command[name] if com != "times"
                ]
            case dict():
                return [
                    PatternNodeBuilderNoParents(command_dict=com,
                                                shared_context=shared_context).build()
                    for com in command[name].items() if com != "times"
                ]

        raise ValueError("Command is not a list or a dict")

    @staticmethod
    def _get_simple_child(name: str, shared_context: SharedContext) -> List[PatternNodeTmpUntyped]:

        pattern_node_data = PatternNodeData(
            name=name,
            times=TimesType(_min_times=1, _max_times=1),
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
