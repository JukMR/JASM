from pathlib import Path

import yaml


def load_test_configs(file_path: str, yaml_config_field: str):
    """Load test configurations from a YAML file."""
    test_folder = Path("tests")
    with open(test_folder / file_path, "r", encoding="utf-8") as file_descriptor:
        return yaml.safe_load(file_descriptor)[yaml_config_field]
