import re
import argparse
from typing import Optional

from parsing.binary_parser import Parser, ParserImplementation, DissasembleImplementation
from Yaml2Regex import Yaml2Regex

from logging_config import enable_debugging, enable_info_level


def run_regex_rule(regex_rule: str, stringify_binary: str) -> bool:
    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return len(result) != 0


def parse_args_from_console() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pattern', required=True, help='Input pattern for parsing')
    parser.add_argument('--debug', default=False, action='store_true', help='Set debugging level')
    parser.add_argument('--info', default=False, action='store_true', help='Set info level')


    # Create a mutually exclusive group for the two arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add the two arguments to the group
    group.add_argument('-b', '--binary', help='Input binary for parsing')
    group.add_argument('-s', '--assembly', help='Input assembly for parsing')

    args = parser.parse_args()

    return args


def match(pattern_pathStr: str,
          binary: Optional[str] = None,
          assembly: Optional[str] = None,
          debug: bool = False,
          info: bool = True
          ) -> bool:

    if info:
        enable_info_level()
    if debug:
        enable_debugging()

    regex_rule = Yaml2Regex(pattern_pathStr=pattern_pathStr).produce_regex()

    parser_implementation = Parser(parser=ParserImplementation(), disassembler=DissasembleImplementation())

    if assembly:
        stringify_binary = parser_implementation.parse(file=assembly)
    elif binary:
        parser_implementation.dissasemble(binary=binary, output_path='tmp_dissasembly.s')
        stringify_binary = parser_implementation.parse(file='tmp_dissasembly.s')
    else:
        raise ValueError("Some error occured")

    did_match = run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary)
    print(did_match)

    return did_match


if __name__ == "__main__":
    args = parse_args_from_console()
    match(pattern_pathStr=args.pattern, assembly=args.assembly, binary=args.binary, debug=args.debug)
