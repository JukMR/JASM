'Global definition file'
import sys
from typing import Any, Dict, List, TypeAlias
from pathlib import Path

IGNORE_ARGS = r'[^\|]*\|'

MAX_PYTHON_INT = sys.maxsize * 2

Pattern: TypeAlias = List[Any] | Dict[str, Any] | str
PathStr: TypeAlias = str | Path
