'Not Directive Processor Implementation'

from src.regex.directive_processor import DirectiveProcessor
from src.global_definitions import PatternDict

class NotDirectiveProcessor(DirectiveProcessor):
    '$not Instruction Processor'

    def __init__(self, not_pattern: PatternDict) -> None:
        exclude_list = not_pattern['inst']
        times = super().get_times(pattern=not_pattern)

        super().__init__(pattern=not_pattern, include_list=None, exclude_list=exclude_list,
                         times=times, operands=None)
