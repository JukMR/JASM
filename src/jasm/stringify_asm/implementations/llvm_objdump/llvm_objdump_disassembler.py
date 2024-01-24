from jasm.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class LLvmObjdumpDisassembler(ShellDisassembler):
    """Disassemble binaries using llvm-objdump from shell"""

    def __init__(self, flags: str) -> None:
        super().__init__(program="llvm-objdump", flags=flags)
