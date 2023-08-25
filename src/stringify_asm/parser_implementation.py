"Parser Implementation module"

from typing import List, Optional
from pyparsing import ParseResults, ParserElement

from src.logging_config import logger
from src.stringify_asm.pyparsing_binary_rules import parsed
from src.global_definitions import PathStr
from src.stringify_asm.observer_abstract import InstructionObserver, Instruction
from src.measure_performance import measure_performance


class ParserImplementation:
    "Parse Implementation"

    def __init__(self) -> None:
        self.parsed_binary: Optional[ParseResults] = None
        self.instruction_observers: Optional[List[InstructionObserver]] = None

    def _open_assembly(self, file: PathStr) -> str:
        "Read the binary file"

        with open(file, "r", encoding="utf-8") as file_d:
            binary = file_d.read()

        return binary

    @measure_performance(perf_title="Pyparsing")
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
            raise ValueError(
                f"Return ParseResults are not of ParseResult type: {parsed_instructions}"
                + f"The type returned is {type(parsed_instructions)}"
            )

        return parsed_instructions

    def _parse_instruction(self, inst: ParserElement) -> Instruction:
        parsed_inst = inst.as_list()[0]  # type: ignore  // as_list() method is not recognized as method of ParseElement
        mnemonic = parsed_inst[0]
        operands = parsed_inst[1:]
        return Instruction(mnemonic=mnemonic, operands=operands)

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
        if self.parsed_binary is None:
            raise NotImplementedError("Error. Call parse_binary() to setup a binary first")

        instruction_list = [self._parse_instruction(inst) for inst in self.parsed_binary]

        string_divided_by_bars = self.run_observers(instruction_list=instruction_list)

        logger.info("The concatenated instructions are:\n %s\n", string_divided_by_bars)
        return string_divided_by_bars

    def set_binary_and_parse_it(self, file: PathStr) -> None:
        "Execute function to parse binary"

        self.parsed_binary = self._run_pyparsing(file=file)

    @measure_performance(perf_title="Parse Instructions")
    def parse(self) -> str:
        "Main parse function"

        return self._generate_string_divided_by_bars()
