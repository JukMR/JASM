"Parser Implementation module"

import re
from typing import List
from pyparsing import ParseResults, ParserElement

from src.logging_config import logger
from src.stringify_asm.pyparsing_binary_rules import parsed
from src.global_definitions import PathStr
from src.stringify_asm.abstracts.observer_abstract import InstructionObserver, Instruction
from src.stringify_asm.abstracts.parser_abstract import Parser
from src.measure_performance import measure_performance


class ParserImplementation(Parser):
    "Parse Implementation"

    def __init__(self, assembly_pathstr: PathStr) -> None:
        super().__init__(assembly_pathstr=assembly_pathstr)
        self.assembly = self._open_assembly(self.assembly_pathstr)
        self.instruction_list = [self._parse_instruction(inst) for inst in self._run_pyparsing()]
        self.instruction_observers: List[InstructionObserver]

    @staticmethod
    def _open_assembly(file: PathStr) -> str:
        "Read the binary file"

        with open(file, "r", encoding="utf-8") as file_d:
            return file_d.read()

    @measure_performance(perf_title="Pyparsing")
    def _execute_pyparsing(self) -> ParseResults:
        parsed.parse_with_tabs()
        parsed_instructions = parsed.parse_string(self.assembly)

        return parsed_instructions

    def _run_pyparsing(self) -> ParseResults:
        parsed_instructions = self._execute_pyparsing()

        # Print the instructions with their arguments
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

    def parse_operands(self, operands: List[str]) -> List[str]:
        "Parse operands"

        return [self._process_operand_elem(operand_elem=operand) for operand in operands]

    def _parse_instruction(self, inst: ParserElement) -> Instruction:
        if inst == "(bad)":
            return Instruction(mnemonic="bad", operands=[])

        parsed_inst = inst.as_list()[0]  # type: ignore  // as_list() method is not recognized as method of ParseElement
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]

        if len(operands) > 0:
            operands_list = self.parse_operands(operands)
            return Instruction(mnemonic=mnemonic, operands=operands_list)
        return Instruction(mnemonic=mnemonic, operands=[])

    def set_observers(self, instruction_observers: List[InstructionObserver]) -> None:
        "Set a list of observers to be notified when an instruction is found"

        self.instruction_observers = instruction_observers

    def run_observers(self, instruction_list: List[Instruction]) -> str:
        "Observe all instructions using all observers"

        if self.instruction_observers is None:
            raise NotImplementedError("instruction_observers not set yet. Call set_observers() first")

        result_str = ""
        for observer in self.instruction_observers:
            for inst in instruction_list:
                observer.observe_instruction(inst=inst)
            result_str += observer.finalize()

        return result_str

    def _generate_string_divided_by_bars(self) -> str:
        string_divided_by_bars = self.run_observers(instruction_list=self.instruction_list)

        logger.info("The concatenated instructions are:\n %s\n", string_divided_by_bars)
        return string_divided_by_bars

    @measure_performance(perf_title="Parse Instructions")
    def parse(self) -> str:
        "Main parse function"

        return self._generate_string_divided_by_bars()
