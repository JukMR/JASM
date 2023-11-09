from src.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class ObjdumpDisassembler(ShellDisassembler):
    """Disassemble binaries using objdump from shell"""

    def __init__(self, flags: str) -> None:
        super().__init__(program="objdump", flags=flags)
