# test_matching.py
from typing import Any, Tuple

import pytest
from conftest import load_test_configs
from ruamel import yaml

from jasm.global_definitions import (InputFileType, MatchConfig,
                                     MatchingReturnMode, MatchingSearchMode)
from jasm.match import MasterOfPuppets


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yaml", yaml_config_field="test_matching"),
    ids=lambda config: config["title"],
)
def test_all_patterns(config: dict):
    """Unified test function for all configurations in configuration.yaml."""
    match_config, expected_result = config_builder(config)
    mop = MasterOfPuppets(match_config=match_config)
    result = mop.perform_matching()
    assert result == expected_result


def update_config(config: dict):
    rtyaml = yaml.YAML()
    rtyaml.indent(mapping=2, sequence=4, offset=2)
    rtyaml.preserve_quotes = True
    with open("tests/configuration.yaml", "r") as f:
        data = rtyaml.load(f)
    for test in data["test_matching"]:
        if test["title"] == config["title"]:
            test["expected-time"] = round(config["expected-time"], 4)
            test["tolerance"] = config["tolerance"]
    with open("tests/configuration.yaml", "w") as f:
        rtyaml.dump(data, f)


def config_builder(config: dict[str, Any]) -> Tuple[MatchConfig, Any]:
    """Build a MatchConfig from the test configuration specs."""

    config_yaml = config["yaml"]
    macros = config.get("macros", None)
    expected_result = config["expected"]
    assembly = config.get("assembly", None)
    binary = config.get("binary", None)
    return_mode = config.get("return_mode", None)
    matching_mode = config.get("matching_mode", None)
    return_only_address = config.get("return_only_address", False)

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
            return_only_address=return_only_address,
            macros=macros,
        ),
        expected_result,
    )
