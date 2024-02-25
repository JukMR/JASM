"Instruction and Instruction Observer module"

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Final, List, Optional


@dataclass
class Instruction:
    "Main instruction class for match patterns"

    addr: str
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        "Method for returning instruction as a string"
        return f"{self.addr}::{self.mnemonic},{','.join(self.operands)}"


class IMatchedObserver(ABC):
    "Observes a match event"

    @property
    @abstractmethod
    def matched(self) -> bool:
        """
        Matched property for observer
        Subclasses must implement this property to get matched status.
        """

    @matched.setter
    @abstractmethod
    def matched(self, value: bool) -> None:
        """Subclasses must implement this property to set match status."""

    @property
    @abstractmethod
    def stringified_instructions(self) -> str:
        """
        Stringified instructions
        Subclasses must implement this property to get stringified instructions.
        """

    @stringified_instructions.setter
    @abstractmethod
    def stringified_instructions(self, value: str) -> None:
        """Subclasses must implement this property to set stringified instructions."""

    @abstractmethod
    def regex_matched(self, addr: str) -> None:
        """Report there was a match event"""

    @abstractmethod
    def finalize(self) -> None:
        """Report that the process was finished"""


class IConsumer(ABC):
    "Base abstract class for Instruction Observers"

    # Importing type here to prevent circular import
    from jasm.stringify_asm.abstracts.abs_observer import IMatchedObserver  # pylint: disable=import-outside-toplevel

    def __init__(self, matched_observer: IMatchedObserver) -> None:
        self._matched_observer: Final = matched_observer

    @abstractmethod
    def consume_instruction(self, inst: Instruction) -> None:
        "Main consumer method"

    @abstractmethod
    def finalize(self) -> None:
        "Finalize consumer"


class IInstructionObserver(ABC):
    "Base abstract class for Instruction Observers"

    @abstractmethod
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        "Main observer method"
