"Main test file"
import re
from typing import Optional
from pathlib import Path
import pytest
import yaml


from src.match import perform_matching, get_instruction_observers
from src.logging_config import logger
from src.stringify_asm.implementations.parser_implementation import ParserImplementation


def load_test_configs(file_path: str | Path, yaml_config_field: str):
    """Load test configurations from a YAML file."""
    test_folder = Path("test")
    with open(test_folder / file_path, "r", encoding="utf-8") as file_descriptor:
        return yaml.safe_load(file_descriptor)[yaml_config_field]


def run_match_test(
    pattern_pathstr: str, assembly: str, expected_result: bool, dissasembler: Optional[str], binary: Optional[str]
) -> None:
    """Run a single match test."""

    if expected_result is None and binary is None:
        raise ValueError("Wrong error configuration. At least one argument should be given")

    result = perform_matching(
        pattern_pathstr=pattern_pathstr, assembly=assembly, disassemble_program=dissasembler, binary=binary
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yml", yaml_config_field="test_configs"),
    ids=lambda config: config["title"],
)
def test_all_patterns(config):
    """Test function for all configurations in configuration.yml."""
    config_yaml = config["yaml"]
    expected_result = config["expected"]
    assembly = config.get("assembly", None)
    binary = config.get("binary", None)
    dissasembler = config.get("dissasembler", None)
    logger.info("Testing assembly: %s with pattern: %s", assembly, config_yaml)
    run_match_test(
        pattern_pathstr=config_yaml,
        assembly=assembly,
        expected_result=expected_result,
        binary=binary,
        dissasembler=dissasembler,
    )


def parse_file_and_get_number_of_lines_with_pyparsing(file: str) -> int:
    """Parse file and return number of lines"""

    parser_implementation = ParserImplementation(assembly_pathstr=file)
    parser_implementation.set_observers(instruction_observers=get_instruction_observers())

    stringify_binary = parser_implementation.parse()

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
