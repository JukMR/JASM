import re
import pytest

from conftest import load_test_configs
from src.stringify_asm.implementations.objdump.objdump_parser import ObjdumpParser
from src.logging_config import logger
from src.match import get_instruction_observers


def parse_file_and_get_number_of_lines_with_pyparsing(file: str) -> int:
    """Parse file and return number of lines"""

    with open(file, "r", encoding="utf-8") as file_descriptor:
        readed_file = file_descriptor.read()
    parser_implementation = ObjdumpParser(assembly=readed_file)
    parser_implementation.set_observers(instruction_observers=get_instruction_observers())
    stringify_binary = parser_implementation.parse_assembly()
    return stringify_binary.count("|")


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yml", yaml_config_field="test_parsing_lines"),
    ids=lambda config: config["title"],
)
def test_correct_number_of_lines_with_regex(config) -> None:
    """Parse file and return number of lines"""
    number_of_lines = config.get("number_of_lines")
    assembly = config.get("assembly")
    with open(assembly, "r", encoding="utf-8") as file_descriptor:
        readed_file = file_descriptor.read()
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
    parsed_number_of_lines = parse_file_and_get_number_of_lines_with_pyparsing(assembly)
    assert number_of_lines == parsed_number_of_lines
