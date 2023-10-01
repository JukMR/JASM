from src.stringify_asm.abstracts.abs_disassemble_and_parser import MainDisassembleParser
from src.stringify_asm.implementations.shell_dissasembler import ShellDissasembler
from src.stringify_asm.implementations.llvm_objdump.llvm_objdump_parser import LlvmObjdumpParser


class LlvmObjdump(MainDisassembleParser):
    """Class to disassemble a binary and parse an assembly using llvm-objdump."""

    def __init__(self, dissasemble: ShellDissasembler, parser: LlvmObjdumpParser) -> None:
        self.disassembler = dissasemble
        self.parser = parser

    def get_assembly(self) -> str:
        self.disassembler.disassemble()

    def parse_asssembly(self) -> str:
        """Implement parser"""
        return self.parser.parse_assembly()
