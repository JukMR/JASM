# from typing import override

from src.jasm.stringify_asm.abstracts.disassembler import Disassembler


class NullDisassembler(Disassembler):
    # @override
    def disassemble(self, input_file: str) -> str:
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()
