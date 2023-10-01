from src.stringify_asm.abstracts.abs_disassemble_and_parser import MainDisassembleParser
from src.stringify_asm.implementations.shell_dissasembler import ShellDissasembler
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser


class GNUObjdump(MainDisassembleParser):
    """Class to disassemble a binary and parse an assembly using objdump."""

    def __init__(self, dissasemble: ShellDissasembler, parser: ObjdumpParser) -> None:
        self.disassembler = dissasemble
        self.parser = parser

    def get_assembly(self) -> None:
        self.disassembler.disassemble()

    def parse_asssembly(self) -> str:
        """Implement parser"""
        return self.parser.parse_assembly()
