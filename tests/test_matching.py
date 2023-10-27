import pytest
from typing import Optional

from src.match import perform_matching
from src.logging_config import logger
from conftest import load_test_configs


def run_match_test(pattern_pathstr: str, assembly: str, expected_result: bool, binary: Optional[str]) -> None:
    """Run a single match test."""
    if not assembly and not binary:
        raise ValueError("Wrong error configuration. At least one argument should be given")
    result = perform_matching(pattern_pathstr=pattern_pathstr, assembly=assembly, binary=binary)
    assert result == expected_result


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yml", yaml_config_field="test_matching"),
    ids=lambda config: config["title"],
)
def test_all_patterns(config):
    """Test function for all configurations in configuration.yml."""
    config_yaml = config["yaml"]
    expected_result = config["expected"]
    assembly = config.get("assembly", None)
    binary = config.get("binary", None)
    logger.info("Testing assembly: %s with pattern: %s", assembly, config_yaml)
    run_match_test(
        pattern_pathstr=config_yaml,
        assembly=assembly,
        expected_result=expected_result,
        binary=binary,
    )
