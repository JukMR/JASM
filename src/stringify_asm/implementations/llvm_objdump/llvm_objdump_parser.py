from typing import List
from src.stringify_asm.abstracts.abs_observer import IConsumer
from src.stringify_asm.abstracts.asm_parser import AsmParser


class LlvmObjdumpParser(AsmParser):
    """Parser implementation for the LlvmObjdump class"""

    def parse(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"
        # TODO: Implement this
