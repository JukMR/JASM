import re
from dataclasses import dataclass
from typing import List, Optional, TypeAlias

from jasm.stringify_asm.abstracts.abs_observer import Instruction


@dataclass
@dataclass
class Section:
    name: str


@dataclass
class Label:
    addr: str
    name: str


ParsedElement: TypeAlias = Instruction | Section | Label | str


def parse_file_lines(file_lines: List[str]) -> List[ParsedElement]:
    return [parse_line(line) for line in file_lines]


def parse_line(line: str) -> ParsedElement:
    return LineParser(line).parse()


HEX_NUMBER = "[0-9a-fA-F]"
TAB = "\t"

FIRST_PADDING = r"^ *"
HEX_ADDR = rf"({HEX_NUMBER}+):{TAB}"

INSTRUCTION_CODE = rf"(?:{HEX_NUMBER}{{2}} ?)+"
POSIBLE_TAB = "\t?"
MNEMONIC = rf"{TAB}([^ ]+)"
SPACES = r" +"
OPERANDS = r"([^# ]+)"
# COMMENTS = r"#.+$"
ANYTHING_ELSE = r".*$"

INSTRUCTION_W_OPERANDS = (
    rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{SPACES}{MNEMONIC}{SPACES}{POSIBLE_TAB}{OPERANDS}{ANYTHING_ELSE}"
)


INSTRUCION_NO_OPERANDS = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{SPACES}{MNEMONIC}{ANYTHING_ELSE}"

LINE_NOP_PADDING = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}$"
LINE_IS_LABER = rf"^({HEX_NUMBER}+) <(.*)>:$"

LINE_IS_TITLE = r"^.*file format.*$"


class LineParser:
    def __init__(self, line: str) -> None:
        self.line = line

    def parse(self) -> ParsedElement:
        """Parse a single line of the objdump output."""
        inst = self.parse_instruction()
        if inst:
            return inst

        inst = self.parse_instruction_no_operands()
        if inst:
            return inst

        label = self.parse_label()
        if label:
            return label

        line = self.parse_nop_padding()
        if line:
            return line

        if self.is_line_broken():
            return self.line

        if self.is_empty_line():
            return self.line

        section = self.parse_section()
        if section:
            return section

        if self.line_is_title():
            return self.line

        print(f"Found a line that is not an instruction, section or label: '{self.line}'")
        return self.line

    def line_is_section(self) -> bool:
        """Check if the line is a section."""
        return "Disassembly of section".lower() in self.line.lower()

    def line_is_title(self) -> bool:
        """Check if the line is a title."""
        return bool(re.match(LINE_IS_TITLE, self.line))

    def is_empty_line(self) -> bool:
        """Check if the line is empty."""
        return self.line in ("\n", "")

    def is_line_broken(self) -> bool:
        """Check if the line is broken."""
        return self.line == "	..."

    def parse_instruction(self) -> Optional[Instruction]:
        """Parse a single instruction."""
        match = re.match(INSTRUCTION_W_OPERANDS, self.line)

        if match:
            addrs = match.group(1)
            mnemonic = match.group(2)
            operands = match.group(3)

            operands_list = self.get_splitted_operands(operands=operands)

            operands_parsed = OperandsParser(operands=operands_list).parse()
            return Instruction(addr=addrs, mnemonic=mnemonic, operands=operands_parsed)
        return None

    @staticmethod
    def get_splitted_operands(operands: str) -> List[str]:
        """Get splitted operands."""
        # Will split between commans only if this commas are not inside a parenthesis
        operands_list = re.split(r",(?![^\(]*\))", operands)
        return operands_list

    def parse_instruction_no_operands(self) -> Optional[Instruction]:
        """Parse a single instruction without operands."""
        match = re.match(INSTRUCION_NO_OPERANDS, self.line)
        if match:
            addrs = match.group(1)
            mnemonic = match.group(2)

            # TODO: check if this is needed or this worst the performance
            # If instruction is bad return a bad instruction
            if mnemonic == "(bad)":
                return Instruction(addr=addrs, mnemonic="bad", operands=[])

            return Instruction(addr=match.group(1), mnemonic=match.group(2), operands=[])
        return None

    def parse_section(self) -> Optional[Section]:
        """Parse a single section."""
        match = re.match("disassembly of section (.*)", self.line.lower())
        if match:
            return Section(name=match.group(1))

        return None

    def parse_label(self) -> Optional[Label]:
        """Parse a single label."""
        match = re.match(LINE_IS_LABER, self.line)
        if match:
            return Label(addr=match.group(1), name=match.group(2))
        return None

    def parse_nop_padding(self) -> Optional[Instruction]:
        """Parse a single nop padding."""
        # This is a line that is not an instruction but is a line that is used to pad the output of objdump

        match = re.match(LINE_NOP_PADDING, self.line)
        if match:
            return Instruction(addr=match.group(1), mnemonic="empty", operands=[])
        return None


class OperandsParser:
    """Parse the operands of an instruction."""

    def __init__(self, operands: List[str]) -> None:
        self.operands = operands

    def parse_operands(self) -> List[str]:
        """Parse the operands of an instruction."""
        return [self._process_operand_elem(operand_elem=operand) for operand in self.operands]

    def _process_operand_elem(self, operand_elem: str) -> str:
        "Process operand element"

        # Operand is memory access
        if operand_elem[0] == "(" and operand_elem[-1] == ")":
            operand_elem.replace("[", "").replace(")", "]")
            return operand_elem

        # The operand have a memory address access plus an inmediate
        if "(" in operand_elem and ")" in operand_elem:
            if "," in operand_elem:
                # Operand is of form 0x0(%rax,%rax,1)
                return self.form_full_operand_with_4_elements(operand_elem)

            # Operand is of form *0x1dc59(%rip)
            return self.form_full_operand_with_1_element(operand_elem)

        # Remove $ from inmediate
        if operand_elem.startswith("$"):
            return operand_elem[1:]

        # Leave % to registers
        if operand_elem.startswith("%"):
            return operand_elem

        if isinstance(operand_elem, List):
            return f"{''.join(operand_elem[1])}+{operand_elem[0]}"
        try:
            int(operand_elem)
            return operand_elem
        except (ValueError, TypeError):
            pass

        try:
            (("0x" + operand_elem).encode("utf-8")).hex()
            return operand_elem
        except ValueError:
            pass
        except TypeError:
            pass

        if operand_elem[0] == "<" and operand_elem[-1] == ">":
            return operand_elem

        if operand_elem[0] == "*" and operand_elem[1] == "%":
            return operand_elem

        if operand_elem == "jmp":
            return operand_elem

        if operand_elem == "11c0":
            return operand_elem

        if operand_elem == "nopw":
            return operand_elem

        raise ValueError("Error in processing operand")

    @staticmethod
    def form_full_operand_with_4_elements(operand_elem) -> str:
        """Form a full operand with 4 elements."""
        find_something_with_parenthesis_regex = r"\([^\)]*\)"
        registry = re.search(find_something_with_parenthesis_regex, operand_elem)
        if not registry:
            raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

        constant_offset = operand_elem.replace(registry[0], "")
        inside_parenthesis = registry.group()

        elements = inside_parenthesis.split(",")

        assert len(elements) == 3
        main_reg, register_multiplier, constant_multiplier = elements

        main_reg = main_reg.replace("(", "")
        constant_multiplier = constant_multiplier.replace(")", "")

        return f"[{main_reg}+{register_multiplier}*{constant_multiplier}+{constant_offset}]"

    @staticmethod
    def form_full_operand_with_1_element(operand_elem) -> str:
        find_something_with_parenthesis_regex = r"\([^\)]*\)"
        registry = re.search(find_something_with_parenthesis_regex, operand_elem)
        if not registry:
            raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

        immediate = operand_elem.replace(registry[0], "")

        register = registry.group()
        if register.startswith("("):
            register = register[1:]
        if register.endswith(")"):
            register = register[:-1]

        return f"[{register}+{immediate}]"

    def parse(self) -> List[str]:
        """Main class method.
        Parse the operands of an instruction."""
        operands_list = self.parse_operands()
        return operands_list
