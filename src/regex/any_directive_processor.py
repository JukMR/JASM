'Any Directive Processor Implementation'

from typing import Literal, Optional, Dict, List

from src.global_definitions import PatternDict
from src.regex.directive_processor import DirectiveProcessor


class AnyDirectiveProcessor(DirectiveProcessor):
    '$any Instruction Processor'

    def __init__(self, any_pattern: PatternDict) -> None:
        include_list = self._get_instruction_list(pattern=any_pattern, pattern_type='include_list')
        exclude_list = self._get_instruction_list(pattern=any_pattern, pattern_type='exclude_list')
        times = super().get_times(pattern=any_pattern)

        super().__init__(pattern=any_pattern, include_list=include_list,
                         exclude_list=exclude_list, times=times, operands=None)

    @staticmethod
    def _get_instruction_list(pattern: PatternDict, pattern_type: Literal['include_list', 'exclude_list']
                              ) -> Optional[List[str]]:
        if not isinstance(pattern, Dict):
            return None

        type_list = pattern.get(pattern_type, None)
        if not isinstance(type_list, Dict):
            return None

        type_list_inst = type_list.get('inst', None)
        if type_list_inst is None:
            return None

        if isinstance(type_list_inst, List):
            return type_list_inst
        raise ValueError(
            f"{type_list_inst} is not a List. It is: {type(type_list_inst)}")
