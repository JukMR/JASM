from typing import List
from jasm.global_definitions import DisassStyle, JASMConfig
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

        # Add section flags if provided
        sections = JASMConfig().get_info("sections")
        if sections:
            flags.extend(self._form_section_flags(sections))
        super().__init__(program="objdump", flags=flags)

    @staticmethod
    def _form_section_flags(sections: List[str]) -> List[str]:
        """Form section flags for objdump command."""
        section_flags = []
        for section in sections:
            section_flags.extend(["-j", section])
        return section_flags
