"Not Directive Processor Implementation"


from src.global_definitions import PatternDict
from src.regex.idirective_processor import IDirectiveProcessor


class NotDirectiveProcessor(IDirectiveProcessor):
    "$not Instruction Processor"

    def __init__(self, not_pattern: PatternDict) -> None:
        super().__init__(
            pattern=not_pattern,
            include_list=None,
            exclude_list=not_pattern["inst"],
            times=super().get_times(pattern=not_pattern),
            operands=None,
        )

    def process(self) -> str:
        assert self.exclude_list
        inst_joined = self.join_instructions(inst_list=self.exclude_list, operand=self.operand_regex)

        if self.times_regex:
            return f"((?!{inst_joined}){self.operand_regex}){self.times_regex}"

        return f"((?!{inst_joined}){self.operand_regex})"
