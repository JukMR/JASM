"Global definition file"

import sys
from typing import Any, Dict, List, TypeAlias, Optional
from pathlib import Path

IGNORE_ARGS = r"[^\|]*\|"
IGNORE_OPERANDS_NUMBER = "[^,]*,"

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict
PathStr: TypeAlias = str | Path

IncludeExcludeListType: TypeAlias = Optional[List[str]]
TimesType: TypeAlias = Optional[Dict[str, int]]
OperandListType: TypeAlias = Optional[List[Any]]
OperandType: TypeAlias = Optional[Dict[str, Any]]
