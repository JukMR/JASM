'Main entry module'
from pathlib import Path
import re
import time
import argparse
from typing import List, Optional, Any

from src.stringify_asm_generation.parsing.binary_parser import Parser, ParserImplementation, DissasembleImplementation
from src.stringify_asm_generation.yaml2regex import Yaml2Regex

from src.logging_config import enable_debugging, enable_info_level, logger, add_log_file


def run_regex_rule(regex_rule: str, stringify_binary: str) -> List[Any]:
    'Function to execute the regex pattern in the assembly'

    start_time = time.time()
    result = re.findall(pattern=regex_rule, string=stringify_binary)
    execution_time = time.time() - start_time

    logger.debug("Finishing running regex in %4f", execution_time)

    return result


def parse_args_from_console() -> argparse.Namespace:
    'Get and parse user arguments'
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', required=True, help='Input pattern for parsing')
    parser.add_argument('--debug', default=False, action='store_true', help='Set debugging level')
    parser.add_argument('--info', default=False, action='store_true', help='Set info level')


    # Create a mutually exclusive group for the two arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the two arguments to the group
    group.add_argument('-b', '--binary', help='Input binary for parsing')
    group.add_argument('-s', '--assembly', help='Input assembly for parsing')

    parsed_args = parser.parse_args()

    return parsed_args


def match(pattern_pathstr: str, binary: Optional[str] = None, assembly: Optional[str] = None,
          debug: bool = False, info: bool = True
          ) -> bool:
    'Main entry function'

    if info:
        enable_info_level()
    if debug:
        enable_debugging()


    start_time = time.time()
    regex_rule = Yaml2Regex(pattern_pathstr=pattern_pathstr).produce_regex()
    execution_time = time.time() - start_time

    logger.debug("Finishing generating regex in %4f", execution_time)

    parser_implementation = Parser(
                                parser=ParserImplementation(),
                                disassembler=DissasembleImplementation()
                                )

    start_time = time.time()

    if assembly:
        stringify_binary = parser_implementation.parse(file=assembly)
    elif binary:
        parser_implementation.dissasemble(binary=binary, output_path='tmp_dissasembly.s')
        stringify_binary = parser_implementation.parse(file='tmp_dissasembly.s')
    else:
        raise ValueError("Some error occured")

    execution_time = time.time() - start_time
    logger.debug("Finishing parsing and generating instructions in %4f", execution_time)

    start_time = time.time()
    match_result = run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary)
    execution_time = time.time() - start_time
    logger.debug("Finishing running regex rule in %4f", execution_time)

    if len(match_result) == 0:
        logger.info("RESULT: Pattern not found\n")
        return False

    logger.info("RESULT: Found a match:")
    for matched_pattern in match_result:
        logger.info("Pattern: %s\n", matched_pattern)
    return True



if __name__ == "__main__":
    date = time.ctime().replace(' ', '_').replace(':','_').lower()
    # Create log file
    logs_folder = Path('logs')
    logs_folder.mkdir(parents=True, exist_ok=True)


    add_log_file(f'{logs_folder.name}/main_log_{date}')
    args = parse_args_from_console()
    print("Starting execution... ")
    match(pattern_pathstr=args.pattern, assembly=args.assembly, binary=args.binary,
          debug=args.debug)
