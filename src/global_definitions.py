"Global definition file"

import sys
from enum import Enum, auto
from typing import Any, Dict, List, Optional, TypeAlias

SKIP_TO_END_OF_OPERAND = "[^,]*,"
SKIP_TO_END_OF_COMMAND = "[^|]*" + r"\|"
SKIP_TO_START_OF_OPERAND = "[^|,]*"
SKIP_TO_ANY_OPERAND_CHARS = "[^|]*"

IGNORE_INST_ADDR = r"[\dabcedf]+::"

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict

IncludeExcludeListType: TypeAlias = Optional[List[str]]
TimesType: TypeAlias = Optional[Dict[str, int]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]


class InputFileType(Enum):
    binary = auto()
    assembly = auto()
