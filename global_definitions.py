import sys
from typing import Any, Dict, List, TypeAlias
from pathlib import Path

global IGNORE_ARGS
IGNORE_ARGS = r'[^\|]*\|'

global MAX_PYTHON_INT
MAX_PYTHON_INT = sys.maxsize * 2

Pattern: TypeAlias = List[Any] | Dict[str, Any] | str
PathStr: TypeAlias = str | Path