"""
Parser Implementation module
"""

from jasm.global_definitions import Instruction
from src.jasm.match.abstracts.i_consumer import IConsumer
from jasm.stringify_asm.abstracts.asm_parser import AsmParser
from jasm.stringify_asm.implementations.gnu_objdump.asm_manual_parser_w_regex import parse_file_lines


class ObjdumpParserManual(AsmParser):  # type: ignore
    """Implementation for parsing assembly instructions."""

    def parse(self, file: str, iConsumer: IConsumer) -> None:
        """Main function to parse the assembly."""

        # Parse the assembly and provide instruction to the consumer

        file_lines = file.split("\n")

        parsed_file_lines = parse_file_lines(file_lines)

        only_instructions = [elem for elem in parsed_file_lines if isinstance(elem, Instruction)]
        for elem in only_instructions:
            iConsumer.consume_instruction(elem)
