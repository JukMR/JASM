"Single Directive Processor Implementation"

from typing import List, Dict, Any
from src.regex.directive_processor import DirectiveProcessor
from src.global_definitions import PatternDict, IncludeExcludeListType, OperandType


class SingleDirectiveProcessor(DirectiveProcessor):
    "Basic Instruction Processor"

    def __init__(self, basic_pattern: PatternDict) -> None:
        include_list = self._get_mnemonic_from_simple_pattern(pattern=basic_pattern)
        self._basic_properties = self._get_instruction_properties(include_list=include_list, pattern=basic_pattern)
        times = self._basic_properties.get("times", None)

        super().__init__(
            pattern=basic_pattern,
            include_list=include_list,
            exclude_list=None,
            times=times,
            operands=self._get_operands(),
        )

    @staticmethod
    def _get_mnemonic_from_simple_pattern(pattern: PatternDict) -> List[str]:
        reserved_patterns = ["operands", "times"]
        pattern_elems = [command for command in list(pattern.keys()) if command not in reserved_patterns]

        if len(pattern_elems) != 1:
            raise ValueError(f"Basic command {pattern_elems} has more than one instruction." + "Should only be 1")

        return pattern_elems

    @staticmethod
    def _get_instruction_properties(include_list: IncludeExcludeListType, pattern: PatternDict) -> Dict[str, Any]:
        if include_list is None:
            raise ValueError(f"Some error happened and this basic instruction: {pattern}" + "doesn't have include_list")

        include_inst = include_list[0]

        instruction_properties = pattern[include_inst]
        if not isinstance(instruction_properties, Dict):
            raise ValueError(f"Instruction properties: '{instruction_properties}' is not a Dict")

        return instruction_properties

    def _get_operands(self) -> OperandType:
        return self._basic_properties.get("operands", None)
