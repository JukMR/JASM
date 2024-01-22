from enum import Enum, auto
from src.stringify_asm.implementations.shell_disassembler import ShellDisassembler


# Move this to another more general folder
class EnumDisasStyle(Enum):
    """Enum for the disassembler style."""

    intel = auto()
    att = auto()


class GNUObjdumpDisassembler(ShellDisassembler):
    """Disassemble binaries using objdump from shell"""

    def __init__(self, enum_disas_style: EnumDisasStyle) -> None:
        # Add interface for handling specific flags

        # Read it from yaml and pass it here
        # The flag to use is -M intel or -M att
        super().__init__(program="objdump", flags="-d")
