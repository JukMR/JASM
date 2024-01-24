from abc import ABC, abstractmethod

from src.jasm.stringify_asm.abstracts.abs_observer import IConsumer
from src.jasm.stringify_asm.abstracts.asm_parser import AsmParser
from src.jasm.stringify_asm.abstracts.disassembler import Disassembler


class IInstructionProducer(ABC):
    @abstractmethod
    def process_file(self, file: str, iConsumer: IConsumer) -> None:
        "Method for parsing instruction from given assembly"


class ComposableProducer(IInstructionProducer):
    """Class to disassemble a binary and parse an assembly using objdump."""

    def __init__(self, disassembler: Disassembler, parser: AsmParser) -> None:
        self.disassembler = disassembler
        self.parser = parser

    def process_file(self, file: str, iConsumer: IConsumer) -> None:
        # Disassemble the binary
        assembly_file = self.disassembler.disassemble(file)

        # Parse the assembly
        self.parser.parse(assembly_file, iConsumer)
        iConsumer.finalize()
