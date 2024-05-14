from src.jasm.match.abstracts.i_consumer import IConsumer
from jasm.stringify_asm.abstracts.asm_parser import AsmParser


class LlvmObjdumpParser(AsmParser):  # type: ignore
    """Parser implementation for the LlvmObjdump class"""

    def parse(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"
        # TODO: Implement this
