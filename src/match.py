"""
Main match module
"""

import re
from typing import List, Optional, Any

from src.regex.yaml2regex import Yaml2Regex
from src.measure_performance import measure_performance
from src.logging_config import logger
from src.stringify_asm.abstracts.abs_observer import InstructionObserver
from src.stringify_asm.implementations.objdump.objdump_disassembler import ObjdumpDisassembler
from src.stringify_asm.implementations.observers import RemoveEmptyInstructions
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser
from src.stringify_asm.implementations.objdump.GNUobjdump import GNUObjdump

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

    return [RemoveEmptyInstructions()]


def initialize_objdump_class(assembly: Optional[str], binary: Optional[str]) -> GNUObjdump:
    """Decide"""
    if assembly:
        return parsing_from_assembly(assembly)
    if binary:
        return parsing_from_binary(binary)

    raise ValueError("Either assembly or binary must be provided.")


def parsing_from_assembly(assembly: str) -> GNUObjdump:
    """Set objdump to start the process from an assembly."""

    # Read file from disk
    with open(assembly, "r", encoding="utf-8") as f:
        assembly_read = f.read()

    parser = ObjdumpParser(assembly=assembly_read)

    objdump_instance = GNUObjdump(get_assembly=None, parser=parser)
    return objdump_instance


def parsing_from_binary(binary: str) -> GNUObjdump:
    """Set objdump to start the process from a binary."""

    objdump_disassembler = ObjdumpDisassembler(binary=binary, flags=DEFAULT_FLAGS)
    assembly = objdump_disassembler.disassemble()

    parser = ObjdumpParser(assembly=assembly)
    objdump_instance = GNUObjdump(get_assembly=objdump_disassembler, parser=parser)

    return objdump_instance


def perform_matching(
    pattern_pathstr: str,
    binary: Optional[str] = None,
    assembly: Optional[str] = None,
) -> bool:
    """Main function to perform regex matching on assembly or binary."""

    # Produce directive regex rule
    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()

    # Get instruction observers
    instruction_observers = get_instruction_observers()

    # Initialize objdump class
    objdump_instance = initialize_objdump_class(assembly=assembly, binary=binary)

    # Parse the assembly
    objdump_instance.parser.set_observers(instruction_observers=instruction_observers)
    assembly_string = objdump_instance.parser.parse_assembly()

    # Get the results
    match_result = execute_regex_on_assembly(regex_rule=regex_rule, assembly_string=assembly_string)

    return log_match_results(match_result=match_result)
