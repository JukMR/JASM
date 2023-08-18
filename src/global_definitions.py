'Global definition file'
import sys
from typing import Any, Dict, List, TypeAlias, Optional
from pathlib import Path

IGNORE_ARGS = r'[^\|]*\|'

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict
PathStr: TypeAlias = str | Path

IncludeListType: TypeAlias = Optional[List[str]]
ExcludeListType: TypeAlias = Optional[List[str]]
TimesType: TypeAlias = Optional[Dict[str, int]]
OperandType: TypeAlias = Optional[Dict[str, Any]]
