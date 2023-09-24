"Any Directive Processor Implementation"

from typing import Literal, Optional, Dict, List

from src.global_definitions import PatternDict, SKIP_TO_END_OF_COMMAND
from src.regex.idirective_processor import IDirectiveProcessor


class AnyDirectiveProcessor(IDirectiveProcessor):
    "$any Instruction Processor"

    def __init__(self, any_pattern: PatternDict) -> None:
        include_list = self._get_instruction_list(pattern=any_pattern, pattern_type="include_list")
        exclude_list = self._get_instruction_list(pattern=any_pattern, pattern_type="exclude_list")
        times = super().get_times(pattern=any_pattern)

        super().__init__(
            pattern=any_pattern,
            include_list=include_list,
            exclude_list=exclude_list,
            times=times,
            operands=None,
        )

        if self.exclude_list:
            self.exclude_list_regex = self.join_instructions(inst_list=self.exclude_list, operand=self.operand_regex)

        if self.include_list:
            self.include_list_regex = self.join_instructions(inst_list=self.include_list, operand=self.operand_regex)

    @staticmethod
    def _get_instruction_list(
        pattern: PatternDict, pattern_type: Literal["include_list", "exclude_list"]
    ) -> Optional[List[str]]:
        "Get `include_list` or `exclude_list` from `pattern`"
        if not isinstance(pattern, Dict):
            return None

        type_list = pattern.get(pattern_type, None)
        if isinstance(type_list, List):
            return type_list

    def _process_with_times_regex(self, times_regex: str) -> str:
        if self.exclude_list:
            return self._process_with_exclude_list() + times_regex
        if self.include_list:
            return f"({self.include_list_regex}){times_regex}"
        return f"({SKIP_TO_END_OF_COMMAND}){times_regex}"

    def _process_without_times_regex(self) -> str:
        if self.exclude_list:
            return self._process_with_exclude_list()
        if self.include_list:
            return f"({self.include_list_regex})"
        return f"({SKIP_TO_END_OF_COMMAND})"

    def _process_with_exclude_list(self) -> str:
        if self.include_list:
            return f"((?!{self.exclude_list_regex})({self.include_list_regex}))"
        return f"((?!{self.exclude_list_regex})({SKIP_TO_END_OF_COMMAND}))"

    def process(self) -> str:
        if self.times_regex:
            return self._process_with_times_regex(self.times_regex)
        return self._process_without_times_regex()
