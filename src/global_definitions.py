'Global definition file'
import sys
from typing import Any, Dict, List, TypeAlias
from pathlib import Path

IGNORE_ARGS = r'[^\|]*\|'

MAX_PYTHON_INT = sys.maxsize * 2

PatternDict: TypeAlias = Dict[str, Any]
Pattern: TypeAlias = List[Any] | PatternDict
PathStr: TypeAlias = str | Path
