"""File2Regex module"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from jasm.global_definitions import EnumDisasStyle


class File2Regex(ABC):
    """Base class for file to regex converters"""

    @staticmethod
    @abstractmethod
    def load_file(file) -> Any:
        "Base method to load a file"

    @abstractmethod
    def produce_regex(self):
        "Main method to produce the regex"

    @abstractmethod
    def get_assembly_style(self) -> Optional[EnumDisasStyle]:
        "Method to get the assembly style intel or att"