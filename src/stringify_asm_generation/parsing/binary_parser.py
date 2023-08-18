'Binary Parser module'
from abc import ABC, abstractmethod
import subprocess
from typing import List, Optional
from dataclasses import dataclass
from pyparsing import ParseResults, ParserElement

from src.logging_config import logger
from src.stringify_asm_generation.parsing.pyparsing_binary_rules import parsed
from src.global_definitions import PathStr
from src.measure_performance import measure_performance



@dataclass
class Instruction:
    'Main instruction class for match patterns'
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        'Method for returning instruction as a string'
        return self.mnemonic + ',' + ','.join(self.operands)


class BinaryParser(ABC):
    'Base class for Binary Parser'
    @abstractmethod
    def parse(self, file: PathStr) -> str:
        'Method for creating parsing assembly implementation'

    @abstractmethod
    def dissasemble(self, binary: str, output_path: PathStr) -> None:
        'Method for generating assembly from a binary implementation'


class Parser(BinaryParser):
    'Main class to implement the BinaryParser'
    def __init__(self, parser: 'ParserImplementation', disassembler: 'DissasembleImplementation'):
        self.parser_implementation = parser
        self.disassembler_implementation = disassembler

    def parse(self, file: PathStr) -> str:
        'Parse implementation'
        self.parser_implementation.set_binary_and_parse_it(file=file)

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

    def _open_assembly(self, file: PathStr) -> str:
    # Read the binary file
        with open(file, "r", encoding='utf-8') as file_d:
            binary = file_d.read()
            logger.debug(binary.encode('utf-8'))

        return binary

    @measure_performance(title="Pyparsing")
    def _execute_pyparsing(self, binary: str) -> ParseResults:
        parsed.parse_with_tabs()
        parsed_instructions = parsed.parse_string(binary)
        logger.debug(parsed_instructions.as_dict())

        return parsed_instructions

    def _run_pyparsing(self, file: PathStr) -> ParseResults:
        binary = self._open_assembly(file)

        parsed_instructions = self._execute_pyparsing(binary=binary)

        # Print the instructions with their arguments
        for inst in parsed_instructions:
            logger.debug("The parsed is: %s", inst)

        if isinstance(parsed_instructions, ParseResults):
            return parsed_instructions

        raise ValueError(f"Return ParseResults: {parsed_instructions}")

    def _join_all_instructions(self, instruction_lst: List[Instruction]) -> str:
        result = ''
        for inst in instruction_lst:
            result += inst.stringify() + '|'
        return result

    def _parse_instruction(self, inst: ParserElement) -> Instruction:
        parsed_inst = inst.as_list()[0] #type: ignore
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]
        return Instruction(mnemonic=mnemonic, operands=operands)

    def _generate_string_divided_by_bars(self) -> str:
        instructions = []
        if self.parsed_binary is None:
            raise NotImplementedError("Error. Execute parse_binary() to setup a binary first")

        for elem in self.parsed_binary:
            inst = self._parse_instruction(elem)
            instructions.append(inst)

        string_divided_by_bars = self._join_all_instructions(instructions)
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
