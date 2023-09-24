"Single Directive Processor Implementation"

from typing import List, Dict, Any
from src.regex.idirective_processor import IDirectiveProcessor
from src.global_definitions import PatternDict, IncludeExcludeListType


class SingleDirectiveProcessor(IDirectiveProcessor):
    "Basic Instruction Processor"

    def __init__(self, basic_pattern: PatternDict) -> None:
        include_list = self._get_mnemonic_from_simple_pattern(pattern=basic_pattern)
        basic_properties = self._get_instruction_properties(include_list=include_list, pattern=basic_pattern)

        super().__init__(
            pattern=basic_pattern,
            include_list=include_list,
            exclude_list=None,
            times=basic_properties.get("times", None),
            operands=basic_properties.get("operands", None),
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

    def process(self) -> str:
        assert self.include_list is not None
        inst_joined = self.join_instructions(inst_list=self.include_list, operand=self.operand_regex)

        if self.times_regex is None:
            return f"({inst_joined})"

        return f"({inst_joined}){self.times_regex}"
