"""
Parser Implementation module
"""

import re
from typing import List
from pyparsing import ParseResults, ParserElement

from src.logging_config import logger
from src.global_definitions import PathStr
from src.measure_performance import measure_performance
from src.stringify_asm.pyparsing_binary_rules import parsed
from src.stringify_asm.abstracts.abs_parser import Parser
from src.stringify_asm.abstracts.abs_observer import InstructionObserver, Instruction


BAD_INSTRUCTION = "(bad)"


class ObjdumpParser(Parser):
    """Implementation for parsing assembly instructions."""

    def __init__(self, assembly_pathstr: PathStr) -> None:
        super().__init__(assembly_pathstr=assembly_pathstr)
        self.assembly = self._read_assembly(self.assembly_pathstr)

        self.instruction_observers: List[InstructionObserver]

    @staticmethod
    def _read_assembly(file: PathStr) -> str:
        """Read the assembly file."""
        with open(file, "r", encoding="utf-8") as file_d:
            return file_d.read()

    @measure_performance(perf_title="Pyparsing")
    def _execute_pyparsing(self) -> ParseResults:
        """Execute pyparsing on the assembly."""
        parsed.parse_with_tabs()
        return parsed.parse_string(self.assembly)

    def _log_parsed_instructions(self) -> ParseResults:
        """Log parsed instructions and ensure they are of type ParseResults."""
        parsed_instructions = self._execute_pyparsing()

        for inst in parsed_instructions:
            logger.debug("The parsed is: %s", inst)

        if not isinstance(parsed_instructions, ParseResults):
            raise ValueError(
                f"Return ParseResults are not of ParseResult type: {parsed_instructions}, {type(parsed_instructions)}"
            )

        return parsed_instructions

    @staticmethod
    def _process_operand_elem(operand_elem: str) -> str:
        "Process operand element"

        if operand_elem[0] == "(" and operand_elem[-1] == ")":
            return operand_elem

        if "(" in operand_elem and ")" in operand_elem:
            registry = re.findall(r"\([^\)]*\)", operand_elem)
            if len(registry) != 1:
                raise ValueError(f"Wrong value for operand {operand_elem}, {type(operand_elem)}")

            inmediate = operand_elem.replace(registry[0], "")

            return f"{registry[0]}+{inmediate}"

        if operand_elem[0] == "$" or operand_elem[0] == "%":
            return operand_elem

        if isinstance(operand_elem, List):
            return f"{''.join(operand_elem[1])}+{operand_elem[0]}"
        try:
            int(operand_elem)
            return operand_elem
        except ValueError:
            pass
        except TypeError:
            pass

        try:
            (("0x" + operand_elem).encode("utf-8")).hex()
            return operand_elem
        except ValueError:
            pass
        except TypeError:
            pass

        if operand_elem[0] == "<" and operand_elem[-1] == ">":
            return operand_elem

        if operand_elem[0] == "*" and operand_elem[1] == "%":
            return operand_elem

        if operand_elem == "jmp":
            return operand_elem

        if operand_elem == "11c0":
            return operand_elem

        if operand_elem == "nopw":
            return operand_elem

        raise ValueError("Error in processing operand")

    def _parse_operands(self, operands: List[str]) -> List[str]:
        """Parse the operands of an instruction."""
        return [self._process_operand_elem(operand_elem=operand) for operand in operands]

    def _remove_tags_from_operands(self, operands_list: List[str]) -> List[str]:
        """Remove extra tags from operands."""
        return [
            operand.replace("$", "").replace("%", "").replace("*", "").replace("(", "").replace(")", "")
            for operand in operands_list
        ]

    def _parse_instruction(self, inst: ParserElement) -> Instruction:
        """Parse a single instruction."""
        if inst == BAD_INSTRUCTION:
            return Instruction(mnemonic="bad", operands=[])

        parsed_inst = inst.as_list()[0]  # type: ignore
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]

        if operands:
            operands_list = self._parse_operands(operands)
            operands_list_no_tags = self._remove_tags_from_operands(operands_list)
            return Instruction(mnemonic=mnemonic, operands=operands_list_no_tags)

        return Instruction(mnemonic=mnemonic, operands=[])

    def set_observers(self, instruction_observers: List[InstructionObserver]) -> None:
        """Set a list of observers to be notified when an instruction is found."""
        self.instruction_observers = instruction_observers

    def _notify_observers(self, instruction_list: List[Instruction]) -> str:
        """Notify all observers with the provided instruction list."""
        if not self.instruction_observers:
            raise NotImplementedError("Observers not set. Call set_observers() first.")

        observed_instructions: List[Instruction] | str = instruction_list
        for observer in self.instruction_observers:
            for inst in observed_instructions:
                if not isinstance(inst, Instruction):
                    raise ValueError("Wrong type for observed_instructions")
                observer.observe_instruction(inst=inst)
                observed_instructions = observer.finalize()

        if isinstance(observed_instructions, str):
            return observed_instructions
        raise ValueError("Wrong type for observed_instructions")

    def _call_observers_and_get_final_string(self, instruction_list: List[Instruction]) -> str:
        """Generate a string representation of the assembly."""

        # Notify the observers of the generated instructions
        assembly_string = self._notify_observers(instruction_list=instruction_list)
        logger.info("The concatenated instructions are:\n %s\n", assembly_string)
        return assembly_string

    @measure_performance(perf_title="Parse Instructions")
    def parse_assembly(self) -> str:
        """Main function to parse the assembly."""

        # Parse the assembly and get the list of instructions
        instruction_list = [self._parse_instruction(inst) for inst in self._execute_pyparsing()]

        final_string = self._call_observers_and_get_final_string(instruction_list)

        return final_string
