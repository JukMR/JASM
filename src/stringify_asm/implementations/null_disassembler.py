from src.stringify_asm.abstracts.disassembler import Disassembler


class NullDisassembler(Disassembler):
    def disassemble(self, file: str) -> str:
        return file
