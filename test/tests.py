"Main test file"
from pyparsing import Optional
from typing import Optional
import pytest
import yaml


import sys

sys.path.append("..")

from src.logging_config import logger
from main import match


def load_test_configs(file_path):
    """Load test configurations from a YAML file."""
    with open(file_path, "r", encoding="utf-8") as file_descriptor:
        return yaml.safe_load(file_descriptor)["test_configs"]


def run_match_test(
    pattern_pathstr: str, assembly: str, expected_result: bool, dissasembler: Optional[str], binary: Optional[str]
) -> None:
    """Run a single match test."""

    if expected_result is None and binary is None:
        raise ValueError("Wrong error configuration. At least one argument should be given")

    result = match(pattern_pathstr=pattern_pathstr, assembly=assembly, dissasemble_program=dissasembler, binary=binary)
    assert result == expected_result


@pytest.mark.parametrize("config", load_test_configs("configuration.yml"), ids=lambda config: config["title"])
def test(config):
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
