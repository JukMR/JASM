import pytest
from conftest import load_test_configs

from jasm.global_definitions import InputFileType
from jasm.logging_config import logger
from jasm.match import MasterOfPuppets


def run_match_test(
    pattern_pathstr: str, input_file: str, input_file_type: InputFileType, expected_result: bool
) -> None:
    """Run a single match test."""
    result = MasterOfPuppets().perform_matching(
        pattern_pathstr=pattern_pathstr, input_file=input_file, input_file_type=input_file_type
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yaml", yaml_config_field="test_matching"),
    ids=lambda config: config["title"],
)
def test_all_patterns(config):
    """Test function for all configurations in configuration.yaml."""
    config_yaml = config["yaml"]
    expected_result = config["expected"]
    assembly = config.get("assembly", None)
    binary = config.get("binary", None)
    logger.info("Testing assembly: %s with pattern: %s", assembly, config_yaml)

    if assembly:
        input_file = assembly
        input_file_type = InputFileType.assembly
    elif binary:
        input_file = binary
        input_file_type = InputFileType.binary
    else:
        raise ValueError("Either assembly or binary must be provided")

    run_match_test(
        pattern_pathstr=config_yaml,
        input_file=input_file,
        input_file_type=input_file_type,
        expected_result=expected_result,
    )
