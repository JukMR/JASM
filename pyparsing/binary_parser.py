
import argparse
from pyparsing import Word, Suppress, OneOrMore, ParserElement, Group, SkipTo, Literal, White
from pyparsing import printables, hexnums, Optional, line_end, python_style_comment
from pyparsing.exceptions import ParseException

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

label = HEX + LESS_THAN + Word(printables, exclude_chars=GREATER_THAN) + GREATER_THAN + COLON + line_end

INIT = Suppress(init_section_title)
TEXT = Suppress(text_section_title)
FINI = Suppress(fini_section_title)

commentary = python_style_comment

instruction_addr = Group(HEX + COLON)


hex_coding = Group(Word(hexnums, exact=2)[1, ...] + SkipTo('\n')) # TODO: fix hex_coding as its taking the first 2 digit of the command

command = Word(printables) # TODO: generate rules for this
instruction_code = command[1, ...]


inst = (
        instruction_addr ("index*")
        + hex_coding ("coding*")
        # + Optional(instruction_code) ("command*")
        # + Optional(commentary) ("comment*")
        + many_line_end
        )

line = label("label") | inst ("inst")
lines = line [1, ...]

init_section = INIT + lines
text_section = TEXT + lines
fini_section = FINI + lines


# Parse the binary file
parsed = ( SkipTo(init_section)
          + init_section
        #   + text_section
        #   + fini_section
          )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--binary', required=True, help='Input binary for parsing')
    args = parser.parse_args()

    binary_file = args.binary


    # Read the binary file
    with open(binary_file, "r", encoding='utf-8') as f:
        binary = f.read()
        print(binary.encode('utf-8'))

    result = parsed.parseString(binary)
    print(result.as_dict())

    # Print the instructions with their arguments
    for inst in result:
        print(f"The parsed is: {inst}")



main()