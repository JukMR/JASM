"""
Main match module
"""

import re
from typing import Any, List, Optional, Sequence

from src.consumer import Consumer
from src.logging_config import logger
from src.measure_performance import measure_performance
from src.regex.yaml2regex import Yaml2Regex
from src.stringify_asm.abstracts.abs_observer import Instruction, InstructionObserver
from src.stringify_asm.abstracts.asm_parser import AsmParser
from src.stringify_asm.abstracts.disassembler import Disassembler
from src.stringify_asm.implementations.null_disassembler import NullDisassembler
from src.stringify_asm.implementations.objdump.ComposableProducer import ComposableProducer
from src.stringify_asm.implementations.objdump.objdump_disassembler import ObjdumpDisassembler
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser
from src.stringify_asm.implementations.observers import RemoveEmptyInstructions

TMP_ASSEMBLY_PATH = "tmp_dissasembly.s"
DEFAULT_FLAGS = "-d"


@measure_performance(perf_title="Run regex")
def execute_regex_on_assembly(regex_rule: str, assembly_string: str) -> List[Any]:
    """Execute the regex pattern on the provided assembly string."""
    return re.findall(pattern=regex_rule, string=assembly_string)


def log_match_results(match_result: List[str]) -> bool:
    """Log the match results and return a boolean indicating if a match was found."""
    if not match_result:
        logger.info("RESULT: Pattern not found\n")
        return False

    logger.info("RESULT: Found a match:")
    for matched_pattern in match_result:
        logger.info("Pattern: %s\n", matched_pattern)
    return True


def get_instruction_observers() -> List[InstructionObserver]:
    """Retrieve a list of instruction observers."""

    return []


def process_file(assembly: Optional[str], binary: Optional[str]) -> List[Instruction]:
    """Decide"""

    disassembler: Disassembler
    parser: AsmParser
    if assembly:
        with open(assembly, "r", encoding="utf-8") as f:
            assembly_read = f.read()

        disassembler = NullDisassembler()
        parser = ObjdumpParser()
        return ComposableProducer(disassembler=disassembler, parser=parser).process_file(file=assembly_read)

    if binary:
        disassembler = ObjdumpDisassembler(flags=DEFAULT_FLAGS)
        parser = ObjdumpParser()
        return ComposableProducer(disassembler=disassembler, parser=parser).process_file(file=binary)

    raise ValueError("Either assembly or binary must be provided")


class InstructionCleaner:
    def __init__(self) -> None:
        self.cleaner_observer = RemoveEmptyInstructions()

    def clean_instructions(self, instruction_list: List[Instruction]) -> Sequence[Optional[Instruction]]:
        """Notify all observers with the provided instruction list."""

        return [
            self.cleaner_observer.observe_instruction(inst)
            for inst in instruction_list
            if self.cleaner_observer.observe_instruction(inst)
        ]


def perform_matching(
    pattern_pathstr: str,
    binary: Optional[str] = None,
    assembly: Optional[str] = None,
) -> bool:
    """Main function to perform regex matching on assembly or binary."""

    # Produce directive regex rule
    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()

    # Initialize objdump class
    instruction_list = process_file(assembly=assembly, binary=binary)

    # Remove empty instructions

    instruction_list_cleaned = InstructionCleaner().clean_instructions(instruction_list)

    # Consumer call observers
    consumer = Consumer(inst_list=instruction_list_cleaned)

    observer_list = get_instruction_observers()
    consumer.set_observers(instruction_observers=observer_list)
    assembly_string = consumer.finalize()

    # Get the results
    match_result = execute_regex_on_assembly(regex_rule=regex_rule, assembly_string=assembly_string)

    return log_match_results(match_result=match_result)
