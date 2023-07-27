from pyparsing import Word, alphas, hexnums, Suppress, Combine, SkipTo, LineEnd, restOfLine

# Define grammar elements
section_header = Suppress("Disassembly of section") + Word(alphas + ".").setResultsName("section_name") + Suppress(":")
instruction_address = Word(hexnums + ":")("address")
instruction_code = Word(hexnums)("code")
instruction_rest = Combine(LineEnd() + restOfLine)
instruction_line = instruction_address + instruction_code + instruction_rest

# Define the main parser for a section
section_parser = section_header + instruction_line[...]

# Read the input data from the file
with open('binary_data.s', 'r') as file:
    input_data = file.read()

# Parse the input data
parsed_data = section_parser.searchString(input_data)

print(parsed_data)
