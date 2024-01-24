import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, TypeAlias

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


def get_file_lines(file: Path) -> List[str]:
    with open(file, "r", encoding="utf-8") as f:
        return f.readlines()


def parse_file_lines(file_lines: List[str]) -> List[ParsedElement]:
    parsed_file_lines = []
    for line in file_lines:
        parsed_file_lines.append(parse_line(line))
    return parsed_file_lines


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
COMMENTS = r"#.+$"
ANYTHING_ELSE = r".*$"

INSTRUCTION_W_OPERANDS = (
    rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{MNEMONIC}{SPACES}{POSIBLE_TAB}{OPERANDS}{ANYTHING_ELSE}"
)

INSTRUCION_NO_OPERANDS = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}{SPACES}{POSIBLE_TAB}{MNEMONIC}{ANYTHING_ELSE}"

LINE_NOP_PADDING = rf"{FIRST_PADDING}{HEX_ADDR}{INSTRUCTION_CODE}$"
LINE_IS_LABER = rf"^({HEX_NUMBER}+) <(.*)>:$"

LINE_IS_TITLE = r"^.*file format.*$"


class LineParser:
    def __init__(self, str_line: str) -> None:
        self.line = str_line

    def parse(self) -> ParsedElement:
        if self.line_is_instruction():
            return self.parse_instruction()

        if self.line_is_instruction_no_operands():
            return self.parse_instruction_no_operands()

        if self.line_is_section():
            return self.parse_section()

        if self.line_is_label():
            return self.parse_label()

        if self.is_empty_line():
            return self.line

        if self.line_is_title():
            return self.line

        if self.line_is_nop_padding():
            return self.line

        print(f"Found a line that is not an instruction, section or label: '{self.line}'")
        return self.line

    def line_is_instruction(self) -> bool:
        return bool(re.match(INSTRUCTION_W_OPERANDS, self.line))

    def line_is_instruction_no_operands(self) -> bool:
        return bool(re.match(INSTRUCION_NO_OPERANDS, self.line))

    def line_is_nop_padding(self) -> bool:
        return bool(re.match(LINE_NOP_PADDING, self.line))

    def line_is_section(self) -> bool:
        return "Disassembly of section".lower() in self.line.lower()

    def line_is_label(self) -> bool:
        return bool(re.match(LINE_IS_LABER, self.line))

    def line_is_title(self) -> bool:
        return bool(re.match(LINE_IS_TITLE, self.line))

    def is_empty_line(self) -> bool:
        return self.line in ("\n", "")

    def parse_instruction(self) -> Instruction:
        match = re.match(INSTRUCTION_W_OPERANDS, self.line)

        if match:
            return Instruction(
                addrs=match.group(1), mnemonic=match.group(2), operands=match.group(3).strip().split(",")
            )
        raise ValueError("Error parsing instruction")

    def parse_instruction_no_operands(self) -> Instruction:
        match = re.match(INSTRUCION_NO_OPERANDS, self.line)
        if match:
            return Instruction(addrs=match.group(1), mnemonic=match.group(2), operands=[])
        raise ValueError("Error parsing instruction")

    def parse_section(self) -> Section:
        match = re.match("disassembly of section (.*)", self.line.lower())
        if match:
            return Section(name=match.group(1))
        raise ValueError("Error parsing section")

    def parse_label(self) -> Label:
        match = re.match(LINE_IS_LABER, self.line)
        if match:
            return Label(addr=match.group(1), name=match.group(2))
        raise ValueError("Error parsing label")
