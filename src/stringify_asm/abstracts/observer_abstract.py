"Instruction and Instruction Observer module"

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Instruction:
    "Main instruction class for match patterns"

    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        "Method for returning instruction as a string"
        return self.mnemonic + "," + ",".join(self.operands)


class InstructionObserver(ABC):
    "Base abstract class for Instruction Observers"

    @abstractmethod
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        "Main observer method"
        return inst

    @abstractmethod
    def finalize(self) -> str:
        "Last method called after all visitors"
        return ""
