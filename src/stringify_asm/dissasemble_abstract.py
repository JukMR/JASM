"Main abstract Dissasembler class"

from abc import ABC, abstractmethod

from src.global_definitions import PathStr


class Dissasembler(ABC):
    "Main dissasembler base abstract class"

    def __init__(self, binary: PathStr, output_path: str) -> None:
        self.binary = binary
        self.output_path = output_path

    @abstractmethod
    def get_assembly(self) -> str:
        "Method for generating assembly from a binary implementation"


class DissasembleMethod(ABC):
    '""Dissasembler Implementation"""'

    def __init__(self, binary: PathStr, output_path: str) -> None:
        self.binary = binary
        self.output_path = output_path

    @abstractmethod
    def dissasemble(self) -> None:
        "Implement dissasemble method"
