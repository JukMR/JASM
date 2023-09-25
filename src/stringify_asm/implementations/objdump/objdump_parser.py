"""
Parser Implementation module
"""

import re
from typing import List, cast
from multiprocessing import Pool
from tqdm import tqdm
from pyparsing import ParseException, ParseResults, ParserElement

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
        parsed.enable_packrat()

        try:
            # process the result if parsing is successful
            result = parsed.parse_string(self.assembly)
            return result

        except ParseException as pe:  # pylint: disable=invalid-name
            print(f"Error parsing input at line {pe.lineno}, column {pe.col}, position {pe.loc}.")
            print(pe.line)
            print(" " * (pe.col - 1) + "^")
            print(pe.msg)
            raise

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
        except (ValueError, TypeError):
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

        instruction_parts_addr = inst.as_list()  # type: ignore

        address = instruction_parts_addr[0]

        if len(instruction_parts_addr) == 2:
            return Instruction(addrs=address, mnemonic="empty", operands=[])

        instruction_parts_command = instruction_parts_addr[2]

        mnemonic = instruction_parts_command[0][0]
        operands = instruction_parts_command[0][1:]

        if inst == BAD_INSTRUCTION:
            return Instruction(addrs=address, mnemonic="bad", operands=[])

        if operands:
            operands_list = self._parse_operands(operands)
            operands_list_no_tags = self._remove_tags_from_operands(operands_list)
            return Instruction(addrs=address, mnemonic=mnemonic, operands=operands_list_no_tags)

        return Instruction(addrs=address, mnemonic=mnemonic, operands=[])

    def set_observers(self, instruction_observers: List[InstructionObserver]) -> None:
        """Set a list of observers to be notified when an instruction is found."""
        self.instruction_observers = instruction_observers

    def _observe_single_instruction(self, observer, instruction):
        return observer.observe_instruction(instruction)

    def _finalize_string(self, list_inst: List[str]) -> str:
        return ",|".join(list_inst) + ",|"

    def _notify_observers(self, instruction_list: List[Instruction]) -> str:
        """Notify all observers with the provided instruction list."""
        if not self.instruction_observers:
            raise NotImplementedError("Observers not set. Call set_observers() first.")

        observed_instructions: List[str] | List[Instruction]
        observed_instructions = instruction_list

        for observer in self.instruction_observers:
            # Create a Pool of processes
            with Pool() as pool:
                # Parallelize the observation of instructions by this observer
                # Using tqdm to show progress
                observed_instructions = list(
                    tqdm(
                        pool.starmap(
                            self._observe_single_instruction,
                            [(observer, inst) for inst in observed_instructions if inst],
                        ),
                        total=len(instruction_list),
                        desc="Processing instructions",
                        unit="inst",
                    )
                )
        # Concatenate the list
        observed_instructions = cast(List[str], observed_instructions)
        return self._finalize_string(observed_instructions)

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
