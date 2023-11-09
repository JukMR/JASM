from abc import ABC, abstractmethod
from typing import List
from src.stringify_asm.abstracts.abs_observer import Instruction
from src.stringify_asm.abstracts.asm_parser import AsmParser
from src.stringify_asm.abstracts.disassembler import Disassembler


class IInstructionProducer(ABC):
    @abstractmethod
    def process_file(self, file: str) -> List[Instruction]:
        "Method for parsing instruction from given assembly"


class ComposableProducer(IInstructionProducer):
    """Class to disassemble a binary and parse an assembly using objdump."""

    def __init__(self, disassembler: Disassembler, parser: AsmParser) -> None:
        self.disassembler = disassembler
        self.parser = parser

    def process_file(self, file) -> List[Instruction]:
        # Disassemble the binary
        assembly_file = self.disassembler.disassemble(file)

        # Parse the assembly
        instruction_list = self.parser.parse(assembly_file)

        return instruction_list
