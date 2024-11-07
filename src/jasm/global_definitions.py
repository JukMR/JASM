"Global definition file"

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Final, List, Optional, TypeAlias

from jasm.logging_config import logger

# set this limit to asterisk to reduce backtracking regex explosion
# WARNING: sometimes setting this value too low would affect negative
# lookaheads failing to match the existing pattern
ASTERISK_WITH_LIMIT: Final = r"{0,1000}"

OPTIONAL_COMMA: Final = r",?"

INSTRUCTION_SEPARATOR: Final = r"\|"
SKIP_TO_END_OF_OPERAND: Final = f"[^,|]{ASTERISK_WITH_LIMIT},"
SKIP_TO_END_OF_PATTERN_NODE: Final = f"[^|]{ASTERISK_WITH_LIMIT}" + INSTRUCTION_SEPARATOR
SKIP_TO_START_OF_OPERAND: Final = f"[^|,]{ASTERISK_WITH_LIMIT}"
SKIP_TO_ANY_OPERAND_CHARS: Final = f"[^|]{ASTERISK_WITH_LIMIT}"

IGNORE_INST_ADDR: Final = r"[\dabcedf]+::"

IGNORE_NAME_PREFIX: Final = f"[^,|]{ASTERISK_WITH_LIMIT}"
IGNORE_NAME_SUFFIX: Final = f"[^,|]{ASTERISK_WITH_LIMIT},"

OPTIONAL_PERCENTAGE_CHAR: Final = "%?"
MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict

IncludeExcludeListType: TypeAlias = Optional[List[str]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]

DictNode: TypeAlias = Dict[str, int] | str | int | Dict[str, list[dict[str, Any]] | list[str]]

PatternNodeName: TypeAlias = str | int

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
class TimesType:
    """Dataclass for time type."""

    _min_times: int
    _max_times: int

    @property
    def min_times(self) -> int:
        return self._min_times

    @min_times.setter
    def min_times(self, value: int) -> None:
        if value <= self._max_times:
            self._min_times = value
        else:
            raise ValueError("min_times must be less than or equal to max_times")

    @property
    def max_times(self) -> int:
        return self._max_times

    @max_times.setter
    def max_times(self, value: int) -> None:
        if value >= self._min_times:
            self._max_times = value
        else:
            raise ValueError("max_times must be greater than or equal to min_times")


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


class BinaryFileFormatNotSupported(Exception):
    "Exception for binary file format not supported by disassembler"


class RegisterCaptureSuffixs(Enum):
    SUFFIX_64 = "64"
    SUFFIX_32 = "32"
    SUFFIX_16 = "16"
    SUFFIX_8H = "8h"
    SUFFIX_8L = "8l"


class RegisterCapturePrefix(Enum):
    genreg = auto()
    indreg = auto()
    stackreg = auto()
    basereg = auto()


def remove_access_suffix(pattern_name: str) -> str:
    "Remove the access suffix from the pattern name"

    parts = pattern_name.split(".")
    possible_register_suffix = [suffix.value for suffix in RegisterCaptureSuffixs]
    if parts[-1] in possible_register_suffix:
        return ".".join(parts[:-1])

    return pattern_name


class PartialMatchingConfig(Enum):
    MnemonicsFullMatch = auto()
    OperandsFullMatch = auto()


class JASMConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JASMConfig, cls).__new__(cls)
            cls.global_info = {}
        return cls._instance

    @staticmethod
    def get_instance():
        if JASMConfig._instance is None:
            JASMConfig()
        return JASMConfig._instance

    def _set_info(self, key, value):
        self.global_info[key] = value

    def get_info(self, key):
        return self.global_info.get(key)

    def load_config(self, config: Dict[str, Any]) -> None:
        """Load configuration into the singleton if they are present and valid."""
        self._load_full_match_options(config)
        self._load_assembly_style(config)
        self._load_valid_addr_range(config)
        self._load_sections(config)

    def _load_full_match_options(self, config: Dict[str, Any]) -> None:
        """Load and validate mnemonics-full-match and operands-full-match options."""
        mnemonics = config.get("mnemonics-full-match", False)
        operands = config.get("operands-full-match", False)

        # Ensure mnemonics and operands are booleans
        if not isinstance(mnemonics, bool) or not isinstance(operands, bool):
            raise ValueError("mnemonics and operands must be booleans")

        self._set_info(PartialMatchingConfig.MnemonicsFullMatch, mnemonics)
        self._set_info(PartialMatchingConfig.OperandsFullMatch, operands)

    def _load_assembly_style(self, config: Dict[str, Any]) -> None:
        """Load assembly style into the singleton."""
        style = config.get("style")
        assembly_style = DisassStyle.att  # Default to att if not specified
        if style:
            if style == "intel":
                assembly_style = DisassStyle.intel
            elif style == "att":
                assembly_style = DisassStyle.att
            else:
                logger.error("Invalid or unsupported style: '%s' in the pattern file", style)

        self._set_info("assembly_style", assembly_style)

    def _load_valid_addr_range(self, config: Dict[str, Any]) -> None:
        """Load valid address range into the singleton."""
        valid_addr = config.get("valid_addr_range")
        if valid_addr:
            valid_addr_range = ValidAddrRange(
                min_addr=valid_addr.get("min"), max_addr=valid_addr.get("max")
            )
            self._set_info("valid_addr_range", valid_addr_range)
        else:
            self._set_info("valid_addr_range", None)

    def _load_sections(self, config: Dict[str, Any]) -> None:
        """Load sections into the singleton."""
        sections = config.get("sections", [])
        if not isinstance(sections,
                          list) or not all(isinstance(section, str) for section in sections):
            raise ValueError("sections must be a list of strings")

        self._set_info("sections", sections)
