from jasm.global_definitions import DisassStyle
from jasm.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class GNUObjdumpDisassembler(ShellDisassembler):  # type: ignore
    """Disassemble binaries using objdump from shell"""

    def __init__(self, enum_disas_style: DisassStyle) -> None:
        # Add interface for handling specific flags

        # Read it from yaml and pass it here
        # The flag to use is -M intel or -M att

        # Default -d flag is used to disassemble the binary executable parts
        default_flags = ["-d"]

        flags = default_flags

        match enum_disas_style:
            case DisassStyle.intel:
                flags.extend(["-M", "Intel"])
            case DisassStyle.att:
                flags.extend(["-M", "att"])

        super().__init__(program="objdump", flags=flags)
