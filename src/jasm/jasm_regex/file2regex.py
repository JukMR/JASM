"""File2Regex module"""

from abc import ABC, abstractmethod
from typing import Any


class File2Regex(ABC):
    """Base class for file to regex converters"""

    @staticmethod
    @abstractmethod
    def load_file(file: str) -> Any:
        "Base method to load a file"

    @abstractmethod
    def produce_regex(self) -> None:
        "Main method to produce the regex"
