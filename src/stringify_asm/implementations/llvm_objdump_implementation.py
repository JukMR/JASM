from src.stringify_asm.implementations.shell_program_dissasembler_implementation import ShellProgramDissasembler


class Llvm_Objdump(ShellProgramDissasembler):
    """Llvm Objdump Implementation"""

    def __init__(self, binary: str, output_path: str, flags: str = "") -> None:
        super().__init__(binary, output_path, program="llvm-objdump", flags=f"-d {flags}")

    def disassemble(self) -> None:
        return super().disassemble()

    def parse_asssembly(self) -> str:
        """Implement parser"""
