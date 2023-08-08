
from pyparsing import Word, Suppress, ParserElement, Group, SkipTo, Literal, ParseResults
from pyparsing import printables, hexnums, line_end, python_style_comment, Optional

from pathlib import Path

import sys
sys.path.append('..')
from logging_config import logger

# Set default whitespace
# This is done to be able to parse the end of line '\n'
# By default pyparsing will ignore newlines and whitespaces
i_consider_whitespaces_to_be_only = ' '
ParserElement.set_default_whitespace_chars(i_consider_whitespaces_to_be_only)


# Define the grammar for the binary file
# GRAMMAR

HEX = Word(hexnums)
COLON = ':'
LESS_THAN = '<'
GREATER_THAN = '>'

many_line_end = Suppress(line_end[1, ...])

init_section_title = "Disassembly of section .init:" + many_line_end
text_section_title = "Disassembly of section .text:" + many_line_end
fini_section_title = "Disassembly of section .fini:" + many_line_end

label = Suppress(HEX + LESS_THAN + Word(printables, exclude_chars=GREATER_THAN) + GREATER_THAN + COLON + line_end)

INIT = Suppress(init_section_title)
TEXT = Suppress(text_section_title)
FINI = Suppress(fini_section_title)

commentary = Suppress(python_style_comment)

TAB = Suppress(Literal('\t'))
instruction_addr = Suppress(HEX + COLON) + TAB


hex_coding = Suppress(Group(Word(hexnums, exact=2)[1, ...] + Optional(TAB)))

command = Word(printables, exclude_chars='#') # TODO: generate rules for this
instruction_code = Group(command[1, ...])


inst = (
        instruction_addr ("index*")
        + hex_coding ("coding*")
        + Optional(instruction_code) ("command*")
        + Optional(commentary) ("comment*")
        + many_line_end
        )

line = label("label") | inst ("inst")
lines = line [1, ...]

init_section = INIT + lines
text_section = TEXT + lines
fini_section = FINI + lines

Start_of_file = Suppress(SkipTo(init_section))

# Parse the binary file
parsed = (Start_of_file
          + init_section
          + text_section
          + fini_section
          )

class Parser:

    def __init__(self, file: Path | str) -> None:
        self.file = file

    def parse(self) -> ParseResults:
        # Read the binary file
        with open(self.file, "r", encoding='utf-8') as f:
            binary = f.read()
            logger.debug(binary.encode('utf-8'))

        parsed.parse_with_tabs()
        parsed_instructions = parsed.parseString(binary)
        logger.debug(parsed_instructions.as_dict())

        # Print the instructions with their arguments
        for inst in parsed_instructions:
            logger.debug(f"The parsed is: {inst}")

        return parsed_instructions

    def generate_string_divided_by_bars(self) -> str:
        parsed_string = self.parse()

        string_divided_by_bars = ''
        for elem in parsed_string:
            stringified_list = ''.join(elem)
            string_divided_by_bars += stringified_list + '|'

        return string_divided_by_bars
