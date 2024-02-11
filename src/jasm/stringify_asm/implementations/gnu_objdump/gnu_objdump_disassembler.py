from typing import Optional

from jasm.global_definitions import DisassStyle
from jasm.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class GNUObjdumpDisassembler(ShellDisassembler):
    """Disassemble binaries using objdump from shell"""

    def __init__(self, enum_disas_style: Optional[DisassStyle]) -> None:
        # Add interface for handling specific flags

        # Read it from yaml and pass it here
        # The flag to use is -M intel or -M att

        default_flag = ["-d"]

        match enum_disas_style:
            case DisassStyle.intel:
                default_flag.extend(["-M", "Intel"])
            case DisassStyle.att:
                default_flag.extend(["-M", "att"])

        super().__init__(program="objdump", flags=default_flag)
