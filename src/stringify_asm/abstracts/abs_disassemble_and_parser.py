"Main abstract Dissasembler class"

from abc import ABC, abstractmethod


class MainDisassembleParser(ABC):
    "Main parser base abstract class"

    @abstractmethod
    def get_assembly(self) -> str:
        "Method for disassembling instruction from given assembly"

    @abstractmethod
    def parse_assembly(self) -> str:
        "Method for parsing instruction from given assembly"
