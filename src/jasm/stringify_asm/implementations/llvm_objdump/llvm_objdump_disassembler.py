from jasm.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class LLvmObjdumpDisassembler(ShellDisassembler):  # type: ignore
    """Disassemble binaries using llvm-objdump from shell"""

    def __init__(self, flags: str) -> None:  # pylint: disable=super-init-not-called
        """
          TODO: implement this
        # super().__init__(program="llvm-objdump", flags=flags)
        """
