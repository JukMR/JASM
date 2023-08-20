'Global definition file'
from abc import ABC, abstractmethod
from dataclasses import dataclass
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



@dataclass
class Instruction:
    'Main instruction class for match patterns'
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        'Method for returning instruction as a string'
        return self.mnemonic + ',' + ','.join(self.operands)


class InstructionObserver(ABC):
    'Base abstract class for Instruction Observers'
    @abstractmethod
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        'Main observer method'
        return inst

    @abstractmethod
    def finalize(self) -> str:
        'Last method called after all visitors'
        return ''
