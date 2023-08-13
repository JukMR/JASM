from parsing.binary_parser import Parser
import re
import argparse

from Yaml2Regex import Yaml2Regex

from logging_config import enable_debugging, enable_info_level

def run_regex_rule(regex_rule: str, stringify_binary: str) -> bool:
    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return len(result) != 0

def parse_args_from_console():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yaml', required=True, help='Input yaml for parsing')
    parser.add_argument('-b', '--binary', required=True, help='Input binary for parsing')
    parser.add_argument('--debug', default=False, action='store_true', help='Set debugging level')
    parser.add_argument('--info', default=False, action='store_true', help='Set info level')

    args = parser.parse_args()

    return args


def match(yaml_pathStr: str, binary: str, debug: bool = False, info: bool = True) -> bool:
    if info:
        enable_info_level()
    if debug:
        enable_debugging()

    regex_rule = Yaml2Regex(yaml_pathStr=yaml_pathStr).produce_regex()
    stringify_binary = Parser(file=binary).generate_string_divided_by_bars()

    did_match = run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary)
    print(did_match)

    return did_match

if __name__ == "__main__":
    args = parse_args_from_console()
    match(yaml_pathStr=args.yaml, binary=args.binary, debug=args.debug)