from pyparsing import Word, Suppress, OneOrMore, alphanums, printables, hexnums, Optional, line_end

# Define the grammar for the binary file
HEX = Word(hexnums)
COLON = ":"
LESS_THAN ="<"
GREATER_THAN = ">"

init_title = Suppress("Disassembly of section .init:")
text_title = Suppress("Disassembly of section .text:")
fini_title = Suppress("Disassembly of section.fini:")

header_line = Suppress(HEX) + LESS_THAN + Word(printables, exclude_chars='>') + GREATER_THAN + COLON

INIT = init_title + header_line
TEXT = text_title + header_line
FINI = fini_title + header_line


instruction_index = HEX + COLON
hex_coding = OneOrMore(Word(hexnums, exact=2))

command = Word(printables, exclude_chars=":")
instruction_code = OneOrMore(command)
instruction = instruction_index + hex_coding + instruction_code + line_end

# Read the binary file
with open("binary_data.s", "r") as f:
    binary = f.read()

# Parse the binary file
# parsed = init_title + OneOrMore(instruction) + text_title + OneOrMore(instruction) + fini_title + OneOrMore(instruction)
parsed = OneOrMore(instruction)
result = parsed.parseString(binary)


# Print the instructions with their arguments
for inst in result:
    print(f"The instruction is: {inst}")