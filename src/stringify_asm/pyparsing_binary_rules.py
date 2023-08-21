"Pyparsing assembly matching rules"
from pyparsing import (
    Word,
    Suppress,
    ParserElement,
    Group,
    SkipTo,
    Literal,
    OneOrMore,
    ZeroOrMore,
)
from pyparsing import (
    printables,
    hexnums,
    line_end,
    python_style_comment,
    Optional,
    alphanums,
)


# Set default whitespace
# This is done to be able to parse the end of line '\n'
# By default pyparsing will ignore newlines and whitespaces
I_CONSIDER_WHITESPACES_TO_BE_ONLY = " "
ParserElement.set_default_whitespace_chars(I_CONSIDER_WHITESPACES_TO_BE_ONLY)


# Define the grammar for the binary file
# GRAMMAR

HEX = Word(hexnums)
COLON = ":"
LESS_THAN = "<"
GREATER_THAN = ">"

many_line_end = Suppress(OneOrMore(line_end))

init_section_title = "Disassembly of section .init:" + many_line_end
text_section_title = "Disassembly of section .text:" + many_line_end
fini_section_title = "Disassembly of section .fini:" + many_line_end

label = Suppress(HEX + LESS_THAN + Word(printables, exclude_chars=GREATER_THAN) + GREATER_THAN + COLON + line_end)

INIT = Optional(Suppress(init_section_title))
TEXT = Optional(Suppress(text_section_title))
FINI = Optional(Suppress(fini_section_title))

comment = Suppress(python_style_comment)

TAB = Suppress(Literal("\t"))
instruction_addr = Suppress(HEX + COLON) + TAB


hex_coding = Suppress(Group(OneOrMore(Word(hexnums, exact=2)) + Optional(TAB)))

mnemonic = Word(alphanums)
operand = Word(printables, exclude_chars="#,") + Suppress(Optional(Literal(",")))

operation = Group(mnemonic + ZeroOrMore(operand))


instruction_code = Optional(Group(OneOrMore(operation)))


inst = instruction_addr + hex_coding + instruction_code + Optional(comment) + many_line_end

line = label | inst
lines = OneOrMore(line)

init_section = Optional(INIT + lines)
text_section = Optional(TEXT + lines)
fini_section = Optional(FINI + lines)

Start_of_file = Suppress(SkipTo(Literal("Disassembly")))

# Parse the binary file
parsed = Start_of_file + init_section + text_section + fini_section
