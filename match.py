"Main match module "

import re
from typing import List, Optional, Any

from src.regex.yaml2regex import Yaml2Regex
from src.measure_performance import measure_performance
from src.logging_config import logger
from src.stringify_asm.binary_parser import Parser, ParserImplementation, DissasembleImplementation
from src.stringify_asm.observer_abstract import InstructionObserver
from src.stringify_asm.observers_implementation import InstructionsAppender


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

    parser_implementation = Parser(parser=ParserImplementation(), disassembler=DissasembleImplementation())
    instruction_observers = get_observer_list()

    if assembly:
        stringify_binary = parser_implementation.parse(filename=assembly, instruction_observers=instruction_observers)
    elif binary:
        if dissasemble_program is None:
            raise ValueError("Dissasemble program not set")
        parser_implementation.dissasemble(binary=binary, output_path="tmp_dissasembly.s", program=dissasemble_program)
        stringify_binary = parser_implementation.parse(
            filename="tmp_dissasembly.s", instruction_observers=instruction_observers
        )
    else:
        raise ValueError("Some error occured")

    match_result = run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary)

    return _set_match_results(match_result=match_result)
