from abc import ABC, abstractmethod
import subprocess
from logging_config import logger
from pathlib import Path
from typing import List
from dataclasses import dataclass
from pyparsing import ParseResults, ParserElement

from parsing.pyparsing_binary_rules import parsed

import sys
sys.path.append('..')


@dataclass
class Instruction:
    mnemonic: str
    operands: List[str]

    def stringify(self) -> str:
        return self.mnemonic + ',' + ','.join(self.operands)


class BinaryParser(ABC):
    @abstractmethod
    def parse():
        pass

    @abstractmethod
    def dissamble():
        pass


class Parser(BinaryParser):
    def parse(self, parseImplementation: 'ParserImplementation'):
        return parseImplementation.parse

    def dissamble(self, dissambleImplementation: 'DissableImplementation'):
        return dissambleImplementation.dissamble


class ParserImplementation():
    def __init__(self, file: Path | str) -> None:
        self.file = file
        self.parsed_binary = self._run_pyparsing()

    def _run_pyparsing(self) -> ParseResults:
        # Read the binary file
        with open(self.file, "r", encoding='utf-8') as f:
            binary = f.read()
            logger.debug(binary.encode('utf-8'))

        parsed.parse_with_tabs()
        parsed_instructions = parsed.parse_string(binary)
        logger.debug(parsed_instructions.as_dict())

        # Print the instructions with their arguments
        for inst in parsed_instructions:
            logger.debug(f"The parsed is: {inst}")

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
        logger.info(
            f"The concatenated instructions are:\n {string_divided_by_bars}")
        return string_divided_by_bars

    def parse(self):
        return self._generate_string_divided_by_bars()


class DissableImplementation:
    def __init__(self, binary: str) -> None:
        self.binary = binary

    def write_to_disk(self, data: str) -> None:
        with open('dissasembled.s', 'w', encoding='utf-8') as file:
            file.write(data)

    def _binary_disambler(self, program: str,
                          flags: str
                          ) -> str | None:
        try:
            result = subprocess.run(
                [program, flags, self.binary],
            capture_output=True,
            text=True)

        # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                    self.write_to_disk(result.stdout)
            else:
                # Return the error message, if any
                return f"Error: {result.stderr}"

        except FileNotFoundError:
            return f"Error: program not found. Make sure you have {program} installed and in your system PATH."

    def dissamble_with_objdump(self):
        return self._binary_disambler(program='objdump', flags='d')

    def dissamble_with_llvm(self):
        return self._binary_disambler(program='llvm-objdump', flags='d')

    def dissamble(self):
        self.dissamble_with_objdump()
