"Any Directive Processor Implementation"

from typing import Dict, List, Literal, Optional, cast

from src.global_definitions import SKIP_TO_END_OF_COMMAND, PatternDict
from src.regex.directives_processors.any_elements import RuleElement
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
            self.include_list_regex = self.get_include_list()

    def get_include_list(self) -> str:
        if self.is_include_list_elems_plain():
            return self.join_instructions(inst_list=cast(List[str], self.include_list), operand=self.operand_regex)

        if self.is_include_list_elems_have_operands():
            return self.get_include_list_with_nested_elements()

        raise ValueError("Wrong include_list")

    def get_include_list_with_nested_elements(self) -> str:
        assert self.include_list

        rule_elements: List[RuleElement] = []
        for entry in self.include_list:
            assert isinstance(entry, Dict)
            for entry_name, operands in entry.items():
                assert isinstance(operands, Dict)
                operands_list = operands.get("operands", None)

                rule_elements.append(RuleElement(mnemonic=entry_name, operands=operands_list))

        def form_regex_from_rule_elements(rule_elements: List[RuleElement]) -> str:
            return "|".join(elem.get_regex() for elem in rule_elements)

        return form_regex_from_rule_elements(rule_elements)

    def is_include_list_elems_plain(self) -> bool:
        assert self.include_list
        for entry in self.include_list:
            if isinstance(entry, str):
                return True
        return False

    def is_include_list_elems_have_operands(self) -> bool:
        assert self.include_list
        for entry in self.include_list:
            if isinstance(entry, Dict):
                return True
        return False

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

        # No instruction list to return
        return None

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
            return f"({self.include_list_regex}{SKIP_TO_END_OF_COMMAND})"
        return f"({SKIP_TO_END_OF_COMMAND})"

    def _process_with_exclude_list(self) -> str:
        if self.include_list:
            return f"((?!{self.exclude_list_regex})({self.include_list_regex}))"
        return f"((?!{self.exclude_list_regex})({SKIP_TO_END_OF_COMMAND}))"

    def process(self) -> str:
        if self.times_regex:
            return self._process_with_times_regex(self.times_regex)
        return self._process_without_times_regex()
