import pytest
from conftest import load_test_configs

from jasm.global_definitions import InputFileType, MatchingReturnMode, MatchingSearchMode
from jasm.match import MasterOfPuppets

USE_BENCHMARK = False


def run_match_test(
    pattern_pathstr: str,
    input_file: str,
    input_file_type: InputFileType,
    expected_result: bool | str | list[str],
    return_mode: MatchingReturnMode,
    matching_mode: MatchingSearchMode,
) -> None:
    """Run a single match test."""

    mop_instance = MasterOfPuppets()

    result = mop_instance.perform_matching(
        pattern_pathstr=pattern_pathstr,
        input_file=input_file,
        input_file_type=input_file_type,
        return_mode=return_mode,
        matching_mode=matching_mode,
        return_only_address=True,
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yaml", yaml_config_field="test_matching"),
    ids=lambda config: config["title"],
)
def test_all_patterns(benchmark, config):
    """Test function for all configurations in configuration.yaml."""
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

    if USE_BENCHMARK:
        benchmark(
            run_match_test,
            pattern_pathstr=config_yaml,
            input_file=input_file,
            input_file_type=input_file_type,
            expected_result=expected_result,
            return_mode=return_mode,
            matching_mode=matching_mode,
        )
    else:
        run_match_test(
            pattern_pathstr=config_yaml,
            input_file=input_file,
            input_file_type=input_file_type,
            expected_result=expected_result,
            return_mode=return_mode,
            matching_mode=matching_mode,
        )
