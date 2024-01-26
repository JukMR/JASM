"""
Parser Implementation module
"""

import re
from typing import List

from pyparsing import ParseException, ParserElement, ParseResults
from jasm.measure_performance import measure_performance
from jasm.stringify_asm.abstracts.abs_observer import IConsumer, Instruction
from jasm.stringify_asm.abstracts.asm_parser import AsmParser
from jasm.stringify_asm.pyparsing_binary_rules import parsed

BAD_INSTRUCTION = "(bad)"


class ObjdumpParser(AsmParser):
    """Implementation for parsing assembly instructions."""

    @measure_performance(perf_title="Pyparsing")
    def _execute_pyparsing(self, assembly: str) -> ParseResults:
        """Execute pyparsing on the assembly."""
        parsed.parse_with_tabs()
        parsed.enable_packrat()

        try:
            # process the result if parsing is successful
            result = parsed.parse_string(assembly)
            return result

        except ParseException as pe:  # pylint: disable=invalid-name
            print(f"Error parsing input at line {pe.lineno}, column {pe.col}, position {pe.loc}.")
            print(pe.line)
            print(" " * (pe.col - 1) + "^")
            print(pe.msg)
            raise

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
            return Instruction(addr=address, mnemonic="empty", operands=[])

        instruction_parts_command = instruction_parts_addr[2]

        mnemonic = instruction_parts_command[0][0]
        operands = instruction_parts_command[0][1:]

        if inst == BAD_INSTRUCTION:
            return Instruction(addr=address, mnemonic="bad", operands=[])

        if operands:
            operands_list = self._parse_operands(operands)
            operands_list_no_tags = self._remove_tags_from_operands(operands_list)
            return Instruction(addr=address, mnemonic=mnemonic, operands=operands_list_no_tags)

        return Instruction(addr=address, mnemonic=mnemonic, operands=[])

    # @override
    @measure_performance(perf_title="Parse Instructions")
    def parse(self, file: str, iConsumer: IConsumer) -> None:
        """Main function to parse the assembly."""

        # Parse the assembly and provide instruction to the consumer

        for parse_element in self._execute_pyparsing(assembly=file):
            print(parse_element)
            iConsumer.consume_instruction(self._parse_instruction(parse_element))
