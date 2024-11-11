from typing import Any, List

import pytest
from conftest import load_test_configs

from jasm.global_definitions import InputFileType, MatchConfig, MatchingReturnMode, MatchingSearchMode
from jasm.match import MasterOfPuppets


@pytest.mark.parametrize(
    "config",
    load_test_configs(file_path="configuration.yaml", yaml_config_field="test_capture_groups_references"),
    ids=lambda config: config["title"],
)
def test_capture_group_correct_expanding(config: dict[str, Any]) -> None:

    config_yaml = config["yaml"]
    cc_deref: List[str] = config["cc_deref"]

    match_config = MatchConfig(
        pattern_pathstr=config_yaml,
        input_file="",
        input_file_type=InputFileType.assembly,  # using assembly as default but this is not needed here nor used
        return_mode=MatchingReturnMode.matched_addrs_list,
        matching_mode=MatchingSearchMode.all_finds,
    )

    mop_instance = MasterOfPuppets(match_config)

    for elem in cc_deref:
        assert elem in mop_instance.regex_rule
