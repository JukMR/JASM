'Binary Parser module'
import subprocess
from abc import ABC, abstractmethod
from typing import List, Optional
from pyparsing import ParseResults, ParserElement

from src.logging_config import logger
from src.stringify_asm.pyparsing_binary_rules import parsed
from src.global_definitions import PathStr, InstructionObserver, Instruction
from src.measure_performance import measure_performance


class BinaryParser(ABC):
    'Base class for Binary Parser'
    @abstractmethod
    def parse(self, filename: PathStr, instruction_observers: List[InstructionObserver]) -> str:
        'Method for creating parsing assembly implementation'


    @abstractmethod
    def dissasemble(self, binary: str, output_path: PathStr) -> None:
        'Method for generating assembly from a binary implementation'


class Parser(BinaryParser):
    'Main class to implement the BinaryParser'

    def __init__(self, parser: 'ParserImplementation', disassembler: 'DissasembleImplementation') -> None:
        self.parser_implementation = parser
        self.disassembler_implementation = disassembler

    def parse(self, filename: PathStr, instruction_observers: List[InstructionObserver]) -> str:
        'Parse implementation'

        self.parser_implementation.set_binary_and_parse_it(file=filename)
        self.parser_implementation.set_observers(instruction_observers=instruction_observers)

        stringify_binary = self.parser_implementation.parse()

        if not isinstance(stringify_binary, str):
            raise ValueError(f"Some error occured. stringify_binary is not a string {stringify_binary}"
                             +f" It is of type: {type(stringify_binary)}")

        return stringify_binary

    def dissasemble(self, binary: str, output_path: PathStr) -> None:
        'Dissasembler implementation'

        self.disassembler_implementation.set_binary(binary=binary)
        self.disassembler_implementation.set_output_path(output_path=output_path)

        return self.disassembler_implementation.dissasemble()


class ParserImplementation():
    'Parse Implementation'

    def __init__(self) -> None:
        self.parsed_binary: Optional[ParseResults] = None
        self.instruction_observers: Optional[List[InstructionObserver]] = None

    def _open_assembly(self, file: PathStr) -> str:
        'Read the binary file'

        with open(file, "r", encoding='utf-8') as file_d:
            binary = file_d.read()

        return binary

    @measure_performance(title="Pyparsing")
    def _execute_pyparsing(self, binary: str) -> ParseResults:
        parsed.parse_with_tabs()
        parsed_instructions = parsed.parse_string(binary)

        return parsed_instructions

    def _run_pyparsing(self, file: PathStr) -> ParseResults:
        binary = self._open_assembly(file)

        parsed_instructions = self._execute_pyparsing(binary=binary)

        # Print the instructions with their arguments
        for inst in parsed_instructions:
            logger.debug("The parsed is: %s", inst)

        if not isinstance(parsed_instructions, ParseResults):
            raise ValueError(f"Return ParseResults are not of ParseResult type: {parsed_instructions}" +
                             f"The type returned is {type(parsed_instructions)}")

        return parsed_instructions


    def _parse_instruction(self, inst: ParserElement) -> Instruction:
        parsed_inst = inst.as_list()[0] #type: ignore  // as_list() method is not recognized as method of ParseElement
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]
        return Instruction(mnemonic=mnemonic, operands=operands)

    def set_observers(self, instruction_observers: List[InstructionObserver]) -> None:
        'Set a list of observers to be notified when an instruction is found'

        self.instruction_observers = instruction_observers

    def run_observers(self, instruction_list: List[Instruction]) -> str:
        'Observe all instructions using all observers'

        if self.instruction_observers is None:
            raise NotImplementedError("instruction_observers not set yet. Call set_observers() first")


        result_str = ''
        for observer in self.instruction_observers:
            for inst in instruction_list:
                observer.observe_instruction(inst=inst)
            result_str += observer.finalize()

        return result_str


    def _generate_string_divided_by_bars(self) -> str:
        if self.parsed_binary is None:
            raise NotImplementedError("Error. Call parse_binary() to setup a binary first")

        instruction_list = [self._parse_instruction(inst) for inst in self.parsed_binary]

        string_divided_by_bars = self.run_observers(instruction_list=instruction_list)

        logger.info("The concatenated instructions are:\n %s\n", string_divided_by_bars)
        return string_divided_by_bars

    def set_binary_and_parse_it(self, file: PathStr) -> None:
        'Execute function to parse binary'
        self.parsed_binary = self._run_pyparsing(file=file)

    @measure_performance(title="Parse Instructions")
    def parse(self) -> str:
        'Main parse function'
        return self._generate_string_divided_by_bars()


class DissasembleImplementation:
    'Dissasembler Implementation'

    def __init__(self) -> None:
        self.binary: Optional[str] = None
        self.output_path: Optional[PathStr] = None
        self.dissasemble_program: Optional[str] = None

    def set_binary(self, binary: str) -> None:
        'Set binary for DissasembleImplementation class'
        self.binary = binary

    def set_output_path(self, output_path: PathStr) -> None:
        'Set output_path for DissasembleImplementation class'
        self.output_path = output_path

    def _write_to_disk(self, data: str) -> None:
        if self.output_path is None:
            raise NotImplementedError('No path provided. Execute set_output_path() first')

        with open(self.output_path, 'w', encoding='utf-8') as file:
            file.write(data)

    def _binary_dissasemble(self, program: str, flags: str) -> None:
        if self.binary is None:
            raise NotImplementedError("binary is not set yet. Should call set_binary() first")
        try:
            result = subprocess.run([program, flags, self.binary],
                                    capture_output=True, text=True, check=True)

            # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                self._write_to_disk(result.stdout)
                print(f"File binary successfully dissasembled to {self.output_path}")
            else:
                # Return the error message, if any
                raise ValueError(f"Error while dissasembling file. Error: {result.stderr}")

        except FileNotFoundError as exc:
            raise ValueError(f"Error: program: {program} not found."
                             + "Make sure you to have it installed"
                             + "and in your system PATH.") from exc


    def set_dissasemble_program(self, program: str) -> None:
        """
        Set dissasemble main program.
        Currently objdump and llvm supported and tested
        """

        self.dissasemble_program = program

    def dissasemble(self) -> None:
        'Dissasemble with objdump by_default'

        if self.dissasemble_program is None:
            raise NotImplementedError("dissasemble_program not set yet."
                                      + "Should call set_dissasemble_program() first.")

        return self._binary_dissasemble(program=self.dissasemble_program, flags='-d')
