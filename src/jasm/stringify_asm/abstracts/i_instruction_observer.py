"Instruction and Instruction Observer module"

from abc import ABC, abstractmethod
from typing import Optional

from jasm.global_definitions import Instruction


class IInstructionObserver(ABC):
    "Base abstract class for Instruction Observers"

    @abstractmethod
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        "Main observer method"
