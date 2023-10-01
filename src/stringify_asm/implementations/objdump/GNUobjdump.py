from typing import Optional
from src.stringify_asm.abstracts.abs_disassemble_and_parser import MainDisassembleParser
from src.stringify_asm.implementations.shell_dissasembler import ShellDissasembler
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser


class GNUObjdump(MainDisassembleParser):
    """Class to disassemble a binary and parse an assembly using objdump."""

    def __init__(self, get_assembly: Optional[ShellDissasembler], parser: ObjdumpParser) -> None:
        self.disassembler = get_assembly
        self.parser = parser

    def get_assembly(self) -> str:
        if self.disassembler:
            self.disassembler.disassemble()
        raise ValueError("No disassembler provided.")

    def parse_assembly(self) -> str:
        """Implement parser"""
        return self.parser.parse_assembly()
