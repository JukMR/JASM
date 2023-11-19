import re

import pytest
from conftest import load_test_configs

from src.logging_config import logger
from src.match import InputFileType, perform_matching


def parse_file_and_get_number_of_lines_with_pyparsing(
    pattern_pathstr: str, input_file: str, input_file_type: InputFileType
) -> int:
    """Parse file and return number of lines"""

    perform_matching(
        pattern_pathstr=pattern_pathstr,
        input_file=input_file,
        input_file_type=input_file_type,
    )

    # pylint: disable=import-outside-toplevel
    from main import tester_stringify_inst

    all_instructions = tester_stringify_inst.read()

    return all_instructions.count("|")


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yml", yaml_config_field="test_parsing_lines"),
    ids=lambda config: config["title"],
)
def test_correct_number_of_lines_with_regex(config) -> None:
    """Parse file and return number of lines"""

    def open_file(file_name) -> str:
        """Open file and return its content"""
        with open(file_name, "r", encoding="utf-8") as file_descriptor:
            return file_descriptor.read()

    number_of_lines = config.get("number_of_lines")
    assembly = config.get("assembly")
    readed_file = open_file(assembly)
    matched_lines = len(re.findall(r" [\dabcdef]+:\t([\dabcdef]{2} )* *\t\w*", readed_file))
    assert matched_lines == number_of_lines


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yml", yaml_config_field="test_parsing_lines"),
    ids=lambda config: config["title"],
)
def test_parsing_number_of_lines(config) -> None:
    "Test parsing number of lines for all configurations in configuration.yml."
    assembly = config.get("assembly")
    number_of_lines = config.get("number_of_lines")
    logger.info("Testing assembly number of lines: %s with pattern: %s", assembly, number_of_lines)
    parsed_number_of_lines = parse_file_and_get_number_of_lines_with_pyparsing(
        input_file=assembly, input_file_type=InputFileType.assembly, pattern_pathstr=""
    )
    assert number_of_lines == parsed_number_of_lines
