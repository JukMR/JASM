from abc import ABC, abstractmethod
from typing import Final

from jasm.global_definitions import Instruction


class IConsumer(ABC):
    "Base abstract class for Instruction Observers"

    # Importing type here to prevent circular import
    from src.jasm.match.abstracts.i_matched_observer import IMatchedObserver  # pylint: disable=import-outside-toplevel

    def __init__(self, matched_observer: IMatchedObserver) -> None:
        self._matched_observer: Final = matched_observer

    @abstractmethod
    def consume_instruction(self, inst: Instruction) -> None:
        "Main consumer method"

    @abstractmethod
    def finalize(self) -> None:
        "Finalize consumer"
