"Pyparsing assembly matching rules"
from pyparsing import Word, Suppress, ParserElement, Group, SkipTo, Literal, OneOrMore, ZeroOrMore

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

section_name = Word(printables, exclude_chars=":") + ":"
section_title = "Disassembly of section" + section_name + many_line_end


label = Suppress(HEX + LESS_THAN + Word(printables, exclude_chars=GREATER_THAN) + GREATER_THAN + COLON + line_end)

SECTION_HEADER = Optional(Suppress(section_title))

comment = Suppress(python_style_comment)

TAB = Suppress(Literal("\t"))
instruction_addr = Suppress(HEX + COLON) + TAB


hex_coding = Suppress(Group(OneOrMore(Word(hexnums, exact=2)) + Optional(TAB)))

mnemonic = Word(alphanums)

special_operand_inst = Group(
    Word(printables, exclude_chars=",(")
    + Group("(" + Word(printables, exclude_chars=",)") + "," + Word(printables, exclude_chars=")") + ")")
    + "\n"
)
operand = Word(printables, exclude_chars="#,") + Suppress(Optional(Literal(",")))

operation = Group(mnemonic + ZeroOrMore(special_operand_inst | operand))


instruction_code = Optional(Group(OneOrMore(operation)))


inst = instruction_addr + hex_coding + instruction_code + Optional(comment) + many_line_end

line = label | inst
lines = OneOrMore(line)

section = SECTION_HEADER + lines

Start_of_file = Suppress(SkipTo(Literal("Disassembly")))

# Parse the binary file
parsed = Start_of_file + OneOrMore(section)
