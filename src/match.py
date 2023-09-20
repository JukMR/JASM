"""
Main match module
"""

import re
from typing import List, Optional, Any

from src.regex.yaml2regex import Yaml2Regex
from src.measure_performance import measure_performance
from src.logging_config import logger
from src.stringify_asm.abstracts.observer_abstract import InstructionObserver
from src.stringify_asm.implementations.observers_implementation import InstructionsAppender
from src.stringify_asm.implementations.disassembler_implementation import DissasembleImplementation
from src.stringify_asm.implementations.shell_program_dissasembler_implementation import ShellProgramDissasembler
from src.stringify_asm.implementations.parser_implementation import ParserImplementation

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
    return [InstructionsAppender()]


def perform_matching(
    pattern_pathstr: str,
    disassemble_program: Optional[str] = None,
    binary: Optional[str] = None,
    assembly: Optional[str] = None,
) -> bool:
    """Main function to perform regex matching on assembly or binary."""

    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()
    instruction_observers = get_instruction_observers()

    if assembly:
        parser = ParserImplementation(assembly_pathstr=assembly)
    elif binary:
        if not disassemble_program:
            raise ValueError("Disassemble program not provided.")

        disassemble_method = ShellProgramDissasembler(
            binary=binary, output_path=TMP_ASSEMBLY_PATH, program=disassemble_program, flags=DEFAULT_FLAGS
        )

        disassembler = DissasembleImplementation(
            binary=binary, output_path=TMP_ASSEMBLY_PATH, dissasemble_method=disassemble_method
        )

        disassembler.get_assembly()
        parser = ParserImplementation(assembly_pathstr=TMP_ASSEMBLY_PATH)
    else:
        raise ValueError("Either assembly or binary must be provided.")

    parser.set_observers(instruction_observers=instruction_observers)
    assembly_string = parser.parse()

    match_result = execute_regex_on_assembly(regex_rule=regex_rule, assembly_string=assembly_string)

    return log_match_results(match_result=match_result)
