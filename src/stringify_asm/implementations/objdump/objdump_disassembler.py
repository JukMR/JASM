from src.stringify_asm.implementations.shell_dissasembler import ShellDissasembler


class ObjdumpDisassembler(ShellDissasembler):
    """Disassemble binaries using objdump from shell"""

    def __init__(self, binary: str, flags: str) -> None:
        super().__init__(binary=binary, program="objdump", flags=flags)
