# from typing import override

from jasm.stringify_asm.abstracts.disassembler import Disassembler


class NullDisassembler(Disassembler):  # type: ignore

    def disassemble(self, input_file: str) -> str:
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()
