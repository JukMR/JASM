"Global definition file"

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Final, List, Optional, TypeAlias


# set this limit to asterisk to reduce backtracking regex explosion
# WARNING: sometimes setting this value too low would affect negative
# lookaheads failing to match the existing pattern
ASTERISK_WITH_LIMIT = r"{0,1000}"

INSTRUCTION_SEPARATOR = r"\|"
SKIP_TO_END_OF_OPERAND = f"[^,|]{ASTERISK_WITH_LIMIT},"
SKIP_TO_END_OF_PATTERN_NODE = f"[^|]{ASTERISK_WITH_LIMIT}" + INSTRUCTION_SEPARATOR
SKIP_TO_START_OF_OPERAND = f"[^|,]{ASTERISK_WITH_LIMIT}"
SKIP_TO_ANY_OPERAND_CHARS = f"[^|]{ASTERISK_WITH_LIMIT}"

IGNORE_INST_ADDR = r"[\dabcedf]+::"

IGNORE_NAME_PREFIX = f"[^,|]{ASTERISK_WITH_LIMIT}"
IGNORE_NAME_SUFFIX = f"[^,|]{ASTERISK_WITH_LIMIT},"

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict

IncludeExcludeListType: TypeAlias = Optional[List[str]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]

dict_node: TypeAlias = Dict[str, Any] | str | int


# Move this to a global config class
ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS: Final = True


class InputFileType(Enum):
    """
    Enum for the input file type.

    `binary`: input file is a binary file
    `assembly`: input file is an assembly file
    """

    binary = auto()
    assembly = auto()


class DisassStyle(Enum):
    """Enum for the disassembler style."""

    intel = auto()
    att = auto()


class MatchingSearchMode(Enum):
    """
    Enum for the matching search mode.

    `first_find`: return and stop program on the first match
    `all_finds`: return all matches
    """

    first_find = auto()
    all_finds = auto()


class MatchingReturnMode(Enum):
    """
    Enum for the matching return mode.

    `bool`: return True or False if the pattern is found
    `matched_addrs_list`: return a list of the matched addresses, empty list if no match
    `all_instructions_string`: return all instructions as a string, only for testing purposes
    """

    bool = auto()
    matched_addrs_list = auto()
    all_instructions_string = auto()  # this enum is used for testing only


class CaptureGroupMode(Enum):
    """Enum for the capture group mode."""

    instruction = auto()
    operand = auto()


class PatternNodeTypes(Enum):
    """Enum for the pattern node types. This is used for setting the types of each node in the PatternNode Tree."""

    node = auto()
    operand = auto()
    mnemonic = auto()
    deref = auto()
    deref_property = auto()
    deref_property_capture_group_reference = auto()
    deref_property_capture_group_call = auto()
    times = auto()
    capture_group_reference = auto()
    capture_group_call = auto()
    capture_group_reference_operand = auto()
    capture_group_call_operand = auto()
    root = auto()


class HexType:
    """Class for hex type."""

    def __init__(self, hex_str: str) -> None:
        if hex_str.startswith("0x"):
            only_int_part = hex_str[2:]
        else:
            only_int_part = hex_str
        self.hex = int(only_int_part, 16)

    def __lt__(self, other: "HexType") -> bool:
        return self.hex < other.hex

    def __gt__(self, other: "HexType") -> bool:
        return self.hex > other.hex

    def __eq__(self, other: object) -> bool:
        return self.hex == other


class ValidAddrRange:
    """Class for the valid address observer."""

    def __init__(self, min_addr: str, max_addr: str) -> None:
        self.min = HexType(min_addr)
        self.max = HexType(max_addr)

    def is_in_range(self, addr: str) -> bool:
        """Check if the address is in the valid address range"""
        addr_hex = HexType(addr)

        return self.min.hex <= addr_hex.hex <= self.max.hex


@dataclass
class TimeType:
    """Dataclass for time type."""

    min_times: int
    max_times: int


@dataclass
class MatchConfig:
    """
    Dataclass for match configuration.

    `pattern_pathstr`: the path to the pattern file
    `input_file`: the input file
    `input_file_type`: the input file type
    `return_only_address`: return only the address, not address+instruction
    `return_mode`: the return mode, options are: `bool`, `matched_addrs_list` or `all_instructions_string` (see MatchingReturnMode)
    `matching_mode`: the matching mode, options are: `first_find` or `all_finds` (see MatchingSearchMode)
    `macros`: list of extra macros path files to use
    """

    pattern_pathstr: str
    input_file: str
    input_file_type: InputFileType = InputFileType.assembly
    return_only_address: bool = False
    return_mode: MatchingReturnMode = MatchingReturnMode.bool
    matching_mode: MatchingSearchMode = MatchingSearchMode.first_find
    macros: Optional[List[str]] = None


@dataclass
class Instruction:
    "Main instruction class for match patterns"

    addr: str
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        "Method for returning instruction as a string"
        return f"{self.addr}::{self.mnemonic},{','.join(self.operands)}"
