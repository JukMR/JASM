from abc import ABC, abstractmethod

from src.global_definitions import PathStr


class DisassembleMethod(ABC):
    '""Disassembler Implementation"""'

    def __init__(self, binary: PathStr, output_path: str) -> None:
        self.binary = binary
        self.output_path = output_path

    @abstractmethod
    def disassemble(self) -> None:
        "Implement disassemble method"
