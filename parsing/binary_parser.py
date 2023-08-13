
from dataclasses import dataclass
from typing import List
from pyparsing import Word, Suppress, ParserElement, Group, SkipTo, Literal, ParseResults
from pyparsing import printables, hexnums, line_end, python_style_comment, Optional, alphanums

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

comment = Suppress(python_style_comment)

TAB = Suppress(Literal('\t'))
instruction_addr = Suppress(HEX + COLON) + TAB


hex_coding = Suppress(Group(Word(hexnums, exact=2)[1, ...] + Optional(TAB)))

mnemonic = Word(alphanums)
operand = Word(printables, exclude_chars='#,') + Suppress(Literal(',')[0, 1])

command = Group(mnemonic + operand[0, ...])


instruction_code = Group(command[1, ...])


inst = (
        instruction_addr ("index*")
        + hex_coding ("coding*")
        + Optional(instruction_code) ("command*")
        + Optional(comment) ("comment*")
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


@dataclass
class Instruction:
    mnemonic: str
    operands: List[str]

    def stringify(self):
        return self.mnemonic + ',' + ','.join(self.operands)

class Parser:
    def __init__(self, file: Path | str) -> None:
        self.file = file

    def parse(self) -> ParseResults:
        # Read the binary file
        with open(self.file, "r", encoding='utf-8') as f:
            binary = f.read()
            logger.debug(binary.encode('utf-8'))

        parsed.parse_with_tabs()
        parsed_instructions = parsed.parse_string(binary)
        logger.debug(parsed_instructions.as_dict())

        # Print the instructions with their arguments
        for inst in parsed_instructions:
            logger.debug(f"The parsed is: {inst}")

        return parsed_instructions

    def join_all_instructions(self, instruction_lst: List[Instruction]) -> str:
        result = ''
        for inst in instruction_lst:
            result += inst.stringify() + '|'
        return result

    def parse_Instruction(self, inst: ParserElement) -> Instruction:
        parsed_inst = inst.asList()[0]
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]
        return Instruction(mnemonic=mnemonic, operands=operands)


    def generate_string_divided_by_bars(self) -> str:
        parsed_string = self.parse()

        instructions = []
        for elem in parsed_string:
            inst = self.parse_Instruction(elem)
            instructions.append(inst)

        string_divided_by_bars = self.join_all_instructions(instructions)
        logger.info(f"The concatenated instructions are:\n {string_divided_by_bars}")
        return string_divided_by_bars
