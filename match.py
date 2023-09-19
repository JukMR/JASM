"Main match module "

import re
from typing import List, Optional, Any

from src.regex.yaml2regex import Yaml2Regex
from src.measure_performance import measure_performance
from src.logging_config import logger
from src.stringify_asm.abstracts.observer_abstract import InstructionObserver
from src.stringify_asm.implementations.observers_implementation import InstructionsAppender
from src.stringify_asm.implementations.disassembler_implementation import (
    DissasembleImplementation,
    ShellProgramDissasembler,
)
from src.stringify_asm.implementations.parser_implementation import ParserImplementation


@measure_performance(perf_title="Run regex")
def run_regex_rule(regex_rule: str, stringify_binary: str) -> List[Any]:
    "Function to execute the regex pattern in the assembly"

    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return result


def _set_match_results(match_result: List[str]) -> bool:
    if len(match_result) == 0:
        logger.info("RESULT: Pattern not found\n")
        return False

    logger.info("RESULT: Found a match:")
    for matched_pattern in match_result:
        logger.info("Pattern: %s\n", matched_pattern)
    return True


def get_observer_list() -> List[InstructionObserver]:
    "Get observers_list"
    instruction_observers: List[InstructionObserver] = [InstructionsAppender()]
    return instruction_observers


def match(
    pattern_pathstr: str,
    dissasemble_program: Optional[str],
    binary: Optional[str],
    assembly: Optional[str],
) -> bool:
    "Main entry function"

    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()

    instruction_observers = get_observer_list()

    if assembly:
        parser = ParserImplementation(assembly_pathstr=assembly)
        parser.set_observers(instruction_observers=instruction_observers)
        stringify_binary = parser.parse()
    elif binary:
        if dissasemble_program is None:
            raise ValueError("Dissasemble program not set")

        dissasemble_method_implementation = ShellProgramDissasembler(
            binary=binary, output_path="tmp_dissasembly.s", program=dissasemble_program, flags="-d"
        )

        disassembler = DissasembleImplementation(
            binary=binary, output_path="tmp_dissasembly.s", dissasemble_method=dissasemble_method_implementation
        )

        disassembler.get_assembly()
        parser = ParserImplementation(assembly_pathstr="tmp_dissasembly.s")
        parser.set_observers(instruction_observers=instruction_observers)
        stringify_binary = parser.parse()
    else:
        raise ValueError("Some error occured")

    match_result = run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary)

    return _set_match_results(match_result=match_result)
