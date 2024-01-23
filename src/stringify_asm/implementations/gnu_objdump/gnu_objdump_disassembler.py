from typing import Optional

from src.global_definitions import EnumDisasStyle
from src.stringify_asm.implementations.shell_disassembler import ShellDisassembler


class GNUObjdumpDisassembler(ShellDisassembler):
    """Disassemble binaries using objdump from shell"""

    def __init__(self, enum_disas_style: Optional[EnumDisasStyle]) -> None:
        # Add interface for handling specific flags

        # Read it from yaml and pass it here
        # The flag to use is -M intel or -M att

        default_flag = ["-d"]
        if enum_disas_style == EnumDisasStyle.intel:
            default_flag.extend(["-M", "Intel"])

        elif enum_disas_style == EnumDisasStyle.att:
            default_flag.extend(["-M", "att"])

        super().__init__(program="objdump", flags=default_flag)
