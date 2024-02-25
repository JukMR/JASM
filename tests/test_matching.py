# test_matching.py
from typing import Any, List, Tuple

import pytest
from conftest import load_test_configs

from jasm.global_definitions import InputFileType, MatchConfig, MatchingReturnMode, MatchingSearchMode
from jasm.match import MasterOfPuppets


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yaml", yaml_config_field="test_matching"),
    ids=lambda config: config["title"],
)
def test_all_patterns(config: Any, is_benchmark_enabled: bool, benchmark):
    """Unified test function for all configurations in configuration.yaml."""

    match_config, expected_result = config_builder(config)

    # Direct approach without checking if benchmark is callable
    if is_benchmark_enabled:
        benchmark(run_match_test, match_config, expected_result)
    else:
        run_match_test(match_config, expected_result)


def config_builder(config) -> Tuple[MatchConfig, Any]:
    """Build a MatchConfig from the test configuration specs."""

    config_yaml = config["yaml"]
    expected_result = config["expected"]
    assembly = config.get("assembly", None)
    binary = config.get("binary", None)
    return_mode = config.get("return_mode", None)
    matching_mode = config.get("matching_mode", None)

    # Check if tests uses assembly or binary
    if assembly:
        input_file = assembly
        input_file_type = InputFileType.assembly
    elif binary:
        input_file = binary
        input_file_type = InputFileType.binary
    else:
        raise ValueError("Either assembly or binary must be provided")

    # Check if tests should return list of matched_address or bool
    if return_mode == "list":
        return_mode = MatchingReturnMode.matched_addrs_list
    else:
        return_mode = MatchingReturnMode.bool

    # Check if should look for all occurences or just the first
    if matching_mode == "all":
        matching_mode = MatchingSearchMode.all_finds
    else:
        matching_mode = MatchingSearchMode.first_find

    return (
        MatchConfig(
            pattern_pathstr=config_yaml,
            input_file=input_file,
            input_file_type=input_file_type,
            return_mode=return_mode,
            matching_mode=matching_mode,
        ),
        expected_result,
    )


@pytest.fixture(scope="session")
def is_benchmark_enabled(request) -> bool:
    """Determine if benchmarking is enabled."""
    return request.config.getoption("--enable-benchmark")


def run_match_test(test_config: MatchConfig, expected_result: bool | str | List[str]) -> None:
    """Run a single match test."""

    result = MasterOfPuppets(match_config=test_config).perform_matching()
    assert result == expected_result
