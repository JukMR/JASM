"Main abstract Dissasembler class"

from abc import ABC, abstractmethod

from src.global_definitions import PathStr


class Disassembler(ABC):
    "Main disassembler base abstract class"

    def __init__(self, binary: PathStr, output_path: str) -> None:
        self.binary = binary
        self.output_path = output_path

    @abstractmethod
    def disassemble(self) -> str:
        "Method for generating assembly from a binary implementation"
