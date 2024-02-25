"Global definition file"

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Final, List, Optional, TypeAlias


# set this limit to asterisk to reduce backtracking regex explosion
# WARNING: something setting this value too low would affect negative
# lookaheads failing to match the existing pattern
ASTERISK_WITH_LIMIT = r"{0,1000}"

INSTRUCTION_SEPARATOR = r"\|"
SKIP_TO_END_OF_OPERAND = f"[^,|]{ASTERISK_WITH_LIMIT},"
SKIP_TO_END_OF_PATTERN_NODE = f"[^|]{ASTERISK_WITH_LIMIT}" + INSTRUCTION_SEPARATOR
SKIP_TO_START_OF_OPERAND = f"[^|,]{ASTERISK_WITH_LIMIT}"
SKIP_TO_ANY_OPERAND_CHARS = f"[^|]{ASTERISK_WITH_LIMIT}"

IGNORE_INST_ADDR = r"[\dabcedf]+::"

IGNORE_NAME_PREFIX = f"[^,|]{ASTERISK_WITH_LIMIT}"
IGNORE_NAME_SUFFIX = f"[^,|]{ASTERISK_WITH_LIMIT},"  # set a limit of

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
    binary = auto()
    assembly = auto()


class DisassStyle(Enum):
    """Enum for the disassembler style."""

    intel = auto()
    att = auto()


class HexType:
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
    """Enum for the valid address mode."""

    def __init__(self, min_addr: str, max_addr: str) -> None:
        self.min = HexType(min_addr)
        self.max = HexType(max_addr)

    def is_in_range(self, addr: str) -> bool:
        """Check if the address is in the valid address range"""
        addr_hex = HexType(addr)

        return self.min.hex <= addr_hex.hex <= self.max.hex


@dataclass
class TimeType:
    min_times: int
    max_times: int


class PatternNodeTypes(Enum):
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


class MatchingSearchMode(Enum):
    first_find = auto()
    all_finds = auto()


class MatchingReturnMode(Enum):
    bool = auto()
    matched_addrs_list = auto()
    all_instructions_string = auto()  # this enum is used for testing only


class CaptureGroupMode(Enum):
    instruction = auto()
    operand = auto()


@dataclass
class MatchConfig:
    """Dataclass for match configuration."""

    pattern_pathstr: str
    input_file: str
    input_file_type: InputFileType
    expected_result: bool | str | list[str]
    return_mode: MatchingReturnMode
    matching_mode: MatchingSearchMode
