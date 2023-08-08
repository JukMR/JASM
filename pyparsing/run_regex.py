from binary_parser import Parser
import re
import argparse

import sys
sys.path.append('..')

from YamlHandler import YamlHandler

def run_regex_rule(regex_rule: str, stringify_binary: str) -> bool:
    result = re.findall(pattern=regex_rule, string=stringify_binary)
    return len(result) != 0


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--yaml', required=True, help='Input yaml for parsing')
    parser.add_argument('-b', '--binary', required=True, help='Input binary for parsing')
    args = parser.parse_args()


    regex_rule = YamlHandler(args.yaml).produce_regex()
    stringify_binary = Parser(args.binary).generate_string_divided_by_bars()

    print(run_regex_rule(regex_rule=regex_rule, stringify_binary=stringify_binary))

if __name__ == "__main__":
    main()