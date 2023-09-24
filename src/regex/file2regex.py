"""File2Regex module"""

from typing import Any
from abc import ABC, abstractmethod


class File2Regex(ABC):
    """Base class for file to regex converters"""

    @abstractmethod
    def load_file(self, file) -> Any:
        "Base method to load a file"

    @abstractmethod
    def produce_regex(self):
        "Main method to produce the regex"
