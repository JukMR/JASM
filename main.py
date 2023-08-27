"Main entry module"
import re
import argparse
from typing import List, Optional, Any

from src.regex.yaml2regex import Yaml2Regex
from src.measure_performance import measure_performance
from src.logging_config import configure_logger, logger
from src.stringify_asm.binary_parser import Parser, ParserImplementation, DissasembleImplementation
from src.stringify_asm.observer_abstract import InstructionObserver
from src.stringify_asm.observers_implementation import InstructionsAppender


@measure_performance(perf_title="Run regex")
def run_regex_rule(regex_rule: str, stringify_binary: str) -> List[Any]:
    "Function to execute the regex pattern in the assembly"

    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return result


def parse_args_from_console() -> argparse.Namespace:
    "Get and parse user arguments"

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pattern", required=True, help="Input pattern for parsing")
    parser.add_argument("--debug", default=False, action="store_true", help="Set debugging level")
    parser.add_argument("--dissasemble-program", default="objdump", help="Set the program to use as dissasembler")
    parser.add_argument("--info", default=True, action="store_true", help="Set info level")
    parser.add_argument(
        "--disable_logging_to_file", default=False, action="store_true", help="Disable logging to logfile"
    )
    parser.add_argument(
        "--disable_logging_to_terminal", default=False, action="store_true", help="Disable logging to terminal"
    )

    # Create a mutually exclusive group for the two arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the two arguments to the group
    group.add_argument("-b", "--binary", help="Input binary for parsing")
    group.add_argument("-s", "--assembly", help="Input assembly for parsing")

    parsed_args = parser.parse_args()

    return parsed_args


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


@measure_performance(perf_title="Main function")
def main() -> None:
    "Main function"
    args = parse_args_from_console()

    configure_logger(
        debug=args.debug,
        info=args.info,
        disable_log_to_file=args.disable_logging_to_file,
        disable_log_to_terminal=args.disable_logging_to_terminal,
    )

    print("Starting execution... ")
    match(
        pattern_pathstr=args.pattern,
        assembly=args.assembly,
        binary=args.binary,
        dissasemble_program=args.dissasemble_program,
    )


if __name__ == "__main__":
    main()
