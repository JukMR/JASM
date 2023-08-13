
from pyparsing import Word, Suppress, ParserElement, Group, SkipTo, Literal, OneOrMore, ZeroOrMore
from pyparsing import printables, hexnums, line_end, python_style_comment, Optional, alphanums


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

many_line_end = Suppress(OneOrMore(line_end))

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


hex_coding = Suppress(Group(
                OneOrMore(Word(hexnums, exact=2))
                + Optional(TAB))
                )

mnemonic = Word(alphanums)
operand = Word(printables, exclude_chars='#,') + Suppress(Optional(Literal(',')))

operation = Group(mnemonic + ZeroOrMore(operand))


instruction_code = Group(OneOrMore(operation))


inst = (
        instruction_addr ("index*")
        + hex_coding ("coding*")
        + Optional(instruction_code) ("operation*")
        + Optional(comment) ("comment*")
        + many_line_end
        )

line = label("label") | inst ("inst")
lines = OneOrMore(line)

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

