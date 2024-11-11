# conftest.py
from pathlib import Path
from typing import Any

import yaml


def load_test_configs(file_path: str, yaml_config_field: str) -> Any:
    """Load test configurations from a YAML file."""
    test_folder = Path("tests")
    with open(test_folder / file_path, "r", encoding="utf-8") as file_descriptor:
        return yaml.safe_load(file_descriptor)[yaml_config_field]


def pytest_addoption(parser):
    parser.addoption("--update-baseline", action="store_true", help="Update baseline on runned tests")
