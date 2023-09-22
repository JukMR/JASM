from src.stringify_asm.implementations.shell_dissasembler_implementation import ShellDissasembler
from src.stringify_asm.abstracts.parser_abstract import Parser


class LlvmObjdump:
    """Class to disassemble a binary and parse an assembly using llvm-objdump."""

    def __init__(self, dissasemble: ShellDissasembler, parser: Parser) -> None:
        self.disassembler = dissasemble
        self.parser = parser

    def disassemble(self) -> None:
        self.disassembler.disassemble()

    def parse_asssembly(self) -> str:
        """Implement parser"""
        self.parser.parse_assembly()
