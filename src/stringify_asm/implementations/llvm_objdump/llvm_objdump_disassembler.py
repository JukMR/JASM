from src.stringify_asm.implementations.shell_dissasembler import ShellDissasembler


class LLvmObjdumpDisassembler(ShellDissasembler):
    """Disassemble binaries using llvm-objdump from shell"""

    def __init__(self, binary: str, output_path: str, flags: str) -> None:
        super().__init__(binary=binary, output_path=output_path, program="llvm-objdump", flags=flags)
