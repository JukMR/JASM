"Instruction and Instruction Observer module"

from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Final, List, Optional


@dataclass
class Instruction:
    "Main instruction class for match patterns"

    addrs: str
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        "Method for returning instruction as a string"
        return f"{self.addrs}::{self.mnemonic},{','.join(self.operands)}"


class IMatchedObserver(ABC):
    "Observes a match event"

    @property
    @abstractmethod
    def matched(self) -> bool:
        "Matched property for observer"

    @property
    @abstractmethod
    def stringified_instructions(self) -> str:
        "Stringified instructions"

    @abstractmethod
    def regex_matched(self, addr: str) -> None:
        """Report there was a match event"""

    @abstractmethod
    def finalize(self) -> None:
        """Report that the process was finished"""
        pass


class IConsumer(ABC):
    "Base abstract class for Instruction Observers"

    def __init__(self, matched_observer) -> None:
        self._matched_observer: Final = matched_observer

    @abstractmethod
    def consume_instruction(self, inst: Instruction) -> None:
        "Main consumer method"

    @abstractmethod
    def finalize(self) -> None:
        pass


class IInstructionObserver(ABC):
    "Base abstract class for Instruction Observers"

    @abstractmethod
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        "Main observer method"
