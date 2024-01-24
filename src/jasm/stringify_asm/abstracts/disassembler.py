from abc import ABC, abstractmethod


class Disassembler(ABC):
    @abstractmethod
    def disassemble(self, input_file: str) -> str:
        "Method for disassembling binary from given assembly"
