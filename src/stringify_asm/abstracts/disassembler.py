from abc import ABC, abstractmethod


class Disassembler(ABC):
    @abstractmethod
    def disassemble(self, binary: str) -> str:
        "Method for disassembling binary from given assembly"
