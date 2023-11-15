"Instruction and Instruction Observer module"

from abc import ABC, abstractmethod
import abc
from dataclasses import dataclass
from enum import Enum, auto
from typing import Final, List, Optional

from src.logging_config import logger


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

    @abstractmethod
    def regex_matched(self, addr: str) -> None:
        """"""

    @abstractmethod
    def finalize(self) -> None:
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
