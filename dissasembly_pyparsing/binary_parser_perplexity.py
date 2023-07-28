from pyparsing import Word, Suppress, OneOrMore, alphanums, printables, hexnums, Optional, line_end, python_style_comment, ParserElement, Group

i_consider_whitespaces_to_be_only = ' '
ParserElement.setDefaultWhitespaceChars(i_consider_whitespaces_to_be_only)

# Define the grammar for the binary file
HEX = Word(hexnums)
COLON = ':'
LESS_THAN = '<'
GREATER_THAN = '>'

init_title = Suppress("Disassembly of section .init:")
text_title = Suppress("Disassembly of section .text:")
fini_title = Suppress("Disassembly of section .fini:")

header_line = Suppress(HEX) + LESS_THAN + Word(printables, exclude_chars='>') + GREATER_THAN + COLON

INIT = init_title + header_line
TEXT = text_title + header_line
FINI = fini_title + header_line

commentary = python_style_comment

instruction_index = Suppress(Group(HEX + COLON))
hex_coding = Group(OneOrMore(Word(hexnums, exact=2)))

command = Word(printables)
instruction_code = OneOrMore(command)
instruction = (instruction_index ("index*")
            + hex_coding ("coding*")
            + instruction_code ("command*")
            + Optional(commentary) ("comment*")
            + line_end ("line_end*")
              )

# Read the binary file
with open("binary_data.s", "r") as f:
    binary = f.read()

# Parse the binary file
# parsed = init_title + OneOrMore(instruction) + text_title + OneOrMore(instruction) + fini_title + OneOrMore(instruction)
parsed = OneOrMore(instruction)
result = parsed.parseString(binary)

# Print the instructions with their arguments
print(result.as_dict())
for inst in result:
    print(f"The instruction is: {inst}")