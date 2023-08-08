from binary_parser import parse
import argparse
from pathlib import Path

def generate_string_divided_by_bars():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--binary', required=True, help='Input binary for parsing')
    args = parser.parse_args()

    binary_file = args.binary

    binary_file_path = Path(binary_file)

    parsed_string = parse(binary_file_path)

    result = ''
    for elem in parsed_string:
        stringified_list = ''.join(elem)
        result += stringified_list + '|'

    print(result)


generate_string_divided_by_bars()


