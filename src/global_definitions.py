"Global definition file"

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, TypeAlias

INSTRUCTION_SEPARATOR = r"\|"
COMMA = ","
SKIP_TO_END_OF_OPERAND = "[^,|]*,"
SKIP_TO_END_OF_COMMAND = "[^|]*" + INSTRUCTION_SEPARATOR
SKIP_TO_START_OF_OPERAND = "[^|,]*"
SKIP_TO_ANY_OPERAND_CHARS = "[^|]*"

IGNORE_INST_ADDR = r"[\dabcedf]+::"

IGNORE_NAME_PREFIX = "[^,|]*"
IGNORE_NAME_SUFFIX = "[^,|]*,"

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict

IncludeExcludeListType: TypeAlias = Optional[List[str]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]

dict_node: TypeAlias = Dict[str, Any] | str | int


ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS = True


class InputFileType(Enum):
    binary = auto()
    assembly = auto()


@dataclass
class TimeType:
    min_times: int
    max_times: int


class CommandTypes(Enum):
    node = auto()
    operand = auto()
    mnemonic = auto()
