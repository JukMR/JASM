from parsing.binary_parser import Parser
import re
import argparse

from YamlHandler import YamlHandler

from logging_config import enable_debugging

def run_regex_rule(regex_rule: str, stringify_binary: str) -> bool:
    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return len(result) != 0


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yaml', required=True, help='Input yaml for parsing')
    parser.add_argument('-b', '--binary', required=True, help='Input binary for parsing')
    parser.add_argument('--debug', default=False, action='store_true', help='Enable debugging')

    args = parser.parse_args()

    if args.debug:
        enable_debugging()

    regex_rule = YamlHandler(yaml_pathStr=args.yaml).produce_regex()
    stringify_binary = Parser(file=args.binary).generate_string_divided_by_bars()

    print(run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary))

if __name__ == "__main__":
    main()