"Pyparsing assembly matching rules"
from pyparsing import (
    Group,
    Literal,
    OneOrMore,
    Optional,
    ParserElement,
    SkipTo,
    Suppress,
    Word,
    ZeroOrMore,
    alphanums,
    alphas,
    hexnums,
    line_end,
    printables,
    python_style_comment,
)

ParserElement.enablePackrat()


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

BAD_INSTRUCTION = Literal("(bad)")
TAB = Suppress(Literal("\t"))

many_line_end = Suppress(OneOrMore(line_end))

section_name = Word(printables, exclude_chars=":")
section_title = "Disassembly of section" + Optional(section_name) + ":" + many_line_end


label = Suppress(
    HEX + LESS_THAN + Optional(Word(printables, exclude_chars=GREATER_THAN)) + GREATER_THAN + COLON + many_line_end
)

SECTION_HEADER = Optional(Suppress(section_title))

comment = Suppress(python_style_comment)

instruction_addr = HEX + COLON + TAB


hex_coding = Suppress(Group(OneOrMore(Word(hexnums, exact=2)) + Optional(TAB)))

two_words_in_mnemonic = Word(alphas, min=1, max=4) + Literal(",") + Word(alphas, min=1, max=3)
mnemonic = Word(alphanums)

operand_tag_types = Literal("$") ^ Literal("*") ^ Literal("%")

operand = (
    Suppress(Optional(operand_tag_types)) + Word(printables, exclude_chars="#,") + Suppress(Optional(Literal(",")))
)

operation = Group((two_words_in_mnemonic ^ BAD_INSTRUCTION ^ mnemonic) + ZeroOrMore(operand))


instruction_code = Optional(Group(OneOrMore(operation)))


inst = Group(instruction_addr + hex_coding + instruction_code + Optional(comment) + many_line_end)

ellipsis = Suppress(Literal("\t") + Literal("...") + many_line_end)

bad_instruction = instruction_addr + hex_coding + BAD_INSTRUCTION + Optional(comment) + many_line_end

line = label ^ inst ^ ellipsis ^ bad_instruction

lines = OneOrMore(line)

section = SECTION_HEADER + lines

Start_of_file = Suppress(SkipTo(Literal("Disassembly")))

# Parse the binary file
parsed = Start_of_file + OneOrMore(section)
