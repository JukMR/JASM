from abc import ABC, abstractmethod
import subprocess
import time
from logging_config import logger
from pathlib import Path
from typing import List
from dataclasses import dataclass
from pyparsing import ParseResults, ParserElement

from parsing.pyparsing_binary_rules import parsed
from global_definitions import PathStr
import sys
sys.path.append('..')


def measure_performance(title=None):
    'Function to test performance'
    def decorator(func):
        'Decorator to add a custom title to this function'
        def wrapper(*args, **kwargs):
            'Main wrapper to run perf'
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            if title:
                logger.debug("%s: Function '%s' took %f seconds to execute.", title, func.__name__, execution_time)
            else:
                logger.debug("Function '%s' took %f seconds to execute.", func.__name__, execution_time)

            return result
        return wrapper
    return decorator


@dataclass
class Instruction:
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        return self.mnemonic + ',' + ','.join(self.operands)


class BinaryParser(ABC):
    @abstractmethod
    def parse(self) -> None:
        pass

    @abstractmethod
    def dissasemble() -> None:
        pass


class Parser(BinaryParser):
    def __init__(self, parser: 'ParserImplementation', disassembler: 'DissasembleImplementation'):
        self.parser_implementation = parser
        self.disassembler_implementation = disassembler

    def parse(self, file) -> str:
        self.parser_implementation.parse_binary(file=file)

        return self.parser_implementation.parse()

    def dissasemble(self, binary: str, output_path: PathStr) -> None:
        self.disassembler_implementation.load_binary_and_output_path(binary=binary, output_path=output_path)
        return self.disassembler_implementation.dissasemble()

    # def disassemble_and_parse(self, binary: str, temp_path_to_disassemble: str | Path) -> str:
    #     self.disassemble(binary=binary, output_path=temp_path_to_disassemble)
    #     return self.parse(file=temp_path_to_disassemble)



class ParserImplementation():

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

        return parsed_instructions

    def _join_all_instructions(self, instruction_lst: List[Instruction]) -> str:
        result = ''
        for inst in instruction_lst:
            result += inst.stringify() + '|'
        return result

    def _parse_Instruction(self, inst: ParserElement) -> Instruction:
        parsed_inst = inst.asList()[0]
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]
        return Instruction(mnemonic=mnemonic, operands=operands)

    def _generate_string_divided_by_bars(self) -> str:
        instructions = []
        for elem in self.parsed_binary:
            inst = self._parse_Instruction(elem)
            instructions.append(inst)

        string_divided_by_bars = self._join_all_instructions(instructions)
        logger.info("The concatenated instructions are:\n %s\n", string_divided_by_bars)
        return string_divided_by_bars

    def parse_binary(self, file: PathStr) -> None:
        self.parsed_binary = self._run_pyparsing(file=file)

    def parse(self):
        return self._generate_string_divided_by_bars()


class DissasembleImplementation:
    def load_binary_and_output_path(self, binary: str, output_path: PathStr):
        self.binary = binary
        self.output_path = output_path

    def _write_to_disk(self, data: str) -> None:
        with open(self.output_path, 'w', encoding='utf-8') as file:
            file.write(data)

    def _binary_dissasemble(self, program: str, flags: str) -> str | None:
        try:
            result = subprocess.run([program, flags, self.binary], capture_output=True, text=True)

            # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                self._write_to_disk(result.stdout)
            else:
                # Return the error message, if any
                return f"Error: {result.stderr}"

        except FileNotFoundError:
            return f"Error: program not found. Make sure you have {program} installed and in your system PATH."

    def dissasemble_with_objdump(self):
        return self._binary_dissasemble(program='objdump', flags='-d')

    def dissasemble_with_llvm(self):
        return self._binary_dissasemble(program='llvm-objdump', flags='-d')

    def dissasemble(self):
        self.dissasemble_with_objdump()
