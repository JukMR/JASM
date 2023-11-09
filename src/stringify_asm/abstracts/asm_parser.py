from abc import ABC, abstractmethod
from typing import List

from src.stringify_asm.abstracts.abs_observer import Instruction


class AsmParser(ABC):
    @abstractmethod
    def parse(self, file: str) -> List[Instruction]:
        "Method for parsing instruction from given assembly"
