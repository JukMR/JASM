"""
Parser Implementation module
"""

from src.stringify_asm.parsing_asm_manual_regex import parse_file_lines
from src.stringify_asm.abstracts.abs_observer import IConsumer, Instruction
from src.stringify_asm.abstracts.asm_parser import AsmParser


class ObjdumpParserManual(AsmParser):
    """Implementation for parsing assembly instructions."""

    def parse(self, file: str, iConsumer: IConsumer) -> None:
        """Main function to parse the assembly."""

        # Parse the assembly and provide instruction to the consumer

        file_lines = file.split("\n")

        parsed_file_lines = parse_file_lines(file_lines)

        only_instructions = [elem for elem in parsed_file_lines if isinstance(elem, Instruction)]
        for elem in only_instructions:
            iConsumer.consume_instruction(elem)
