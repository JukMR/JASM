import re
from dataclasses import dataclass
from typing import List, Optional, TypeAlias

from src.stringify_asm.abstracts.abs_observer import Instruction


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
MNEMONIC = rf"{TAB}([^ ]+)"
SPACES = r" +"
POSIBLE_TAB = "\t?"
OPERANDS = r"([^#]*)"
# COMMENTS = r"#.+$"
ANYTHING_ELSE = r".*$"

INSTRUCTION_W_OPERANDS = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{SPACES}{POSIBLE_TAB}{MNEMONIC}{SPACES}{POSIBLE_TAB}{OPERANDS}{ANYTHING_ELSE}"


INSTRUCION_NO_OPERANDS = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{SPACES}{POSIBLE_TAB}{MNEMONIC}{ANYTHING_ELSE}"

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
            operands = match.group(3).strip().split(",")

            operands = OperandsParser(operands=operands).parse()
            return Instruction(addrs=addrs, mnemonic=mnemonic, operands=operands)
        return None

    def parse_instruction_no_operands(self) -> Optional[Instruction]:
        """Parse a single instruction without operands."""
        match = re.match(INSTRUCION_NO_OPERANDS, self.line)
        if match:
            addrs = match.group(1)
            mnemonic = match.group(2)

            # TODO: check if this is needed or this worst the performance
            # If instruction is bad return a bad instruction
            if mnemonic == "(bad)":
                return Instruction(addrs=addrs, mnemonic="bad", operands=[])

            return Instruction(addrs=match.group(1), mnemonic=match.group(2), operands=[])
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
            return Instruction(addrs=match.group(1), mnemonic="empty", operands=[])
        return None


class OperandsParser:
    """Parse the operands of an instruction."""

    def __init__(self, operands: List[str]) -> None:
        self.operands = operands

    def parse_operands(self) -> List[str]:
        """Parse the operands of an instruction."""
        return [self._process_operand_elem(operand_elem=operand) for operand in self.operands]

    def remove_tags_from_operands(self, operands_list: List[str]) -> List[str]:
        """Remove extra tags from operands."""
        return [
            operand.replace("$", "").replace("%", "").replace("*", "").replace("(", "").replace(")", "")
            for operand in operands_list
        ]

    @staticmethod
    def _process_operand_elem(operand_elem: str) -> str:
        "Process operand element"

        if operand_elem[0] == "(" and operand_elem[-1] == ")":
            return operand_elem

        if "(" in operand_elem and ")" in operand_elem:
            registry = re.findall(r"\([^\)]*\)", operand_elem)
            if len(registry) != 1:
                raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

            inmediate = operand_elem.replace(registry[0], "")

            return f"{registry[0]}+{inmediate}"

        if operand_elem[0] == "$" or operand_elem[0] == "%":
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

    def parse(self) -> List[str]:
        """Main class method.
        Parse the operands of an instruction."""
        operands_list = self.parse_operands()
        operands_list_no_tags = self.remove_tags_from_operands(operands_list)
        return operands_list_no_tags
