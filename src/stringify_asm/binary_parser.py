"Binary Parser module"
from abc import ABC, abstractmethod
from typing import List

from src.global_definitions import PathStr
from src.stringify_asm.observer_abstract import InstructionObserver
from src.stringify_asm.parser_implementation import ParserImplementation
from src.stringify_asm.dissasembler_implementation import DissasembleImplementation


class BinaryParser(ABC):
    "Base class for Binary Parser"

    @abstractmethod
    def parse(self, filename: PathStr, instruction_observers: List[InstructionObserver]) -> str:
        "Method for creating parsing assembly implementation"

    @abstractmethod
    def dissasemble(self, binary: str, output_path: PathStr) -> None:
        "Method for generating assembly from a binary implementation"


class Parser(BinaryParser):
    "Main class to implement the BinaryParser"

    def __init__(self, parser: ParserImplementation, disassembler: DissasembleImplementation) -> None:
        self.parser_implementation = parser
        self.disassembler_implementation = disassembler

    def parse(self, filename: PathStr, instruction_observers: List[InstructionObserver]) -> str:
        "Parse implementation"

        self.parser_implementation.set_binary_and_parse_it(file=filename)
        self.parser_implementation.set_observers(instruction_observers=instruction_observers)

        stringify_binary = self.parser_implementation.parse()

        if not isinstance(stringify_binary, str):
            raise ValueError(
                f"Some error occured. stringify_binary is not a string {stringify_binary}"
                + f" It is of type: {type(stringify_binary)}"
            )

        return stringify_binary

    def dissasemble(self, binary: str, output_path: PathStr, program: str) -> None:
        "Dissasembler implementation"

        self.disassembler_implementation.set_binary(binary=binary)
        self.disassembler_implementation.set_output_path(output_path=output_path)
        self.disassembler_implementation.set_dissasemble_program(program=program)

        return self.disassembler_implementation.dissasemble()
