from abc import ABC, abstractmethod


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
