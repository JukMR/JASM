from src.stringify_asm.implementations.shell_program_dissasembler_implementation import ShellProgramDissasembler


class Objdump(ShellProgramDissasembler):

    """Objdump implementation"""

    def __init__(self, binary: str, output_path: str, flags: str = "") -> None:
        super().__init__(binary, output_path, program="objdump", flags=f"{flags}")

    def disassemble(self) -> None:
        return super().disassemble()

    def parse_asssembly(self) -> str:
        """Implement parser"""
