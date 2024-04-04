# conftest.py
from pathlib import Path
from typing import Any

import yaml


def load_test_configs(file_path: str, yaml_config_field: str) -> Any:
    """Load test configurations from a YAML file."""
    test_folder = Path("tests")
    with open(test_folder / file_path, "r", encoding="utf-8") as file_descriptor:
        return yaml.safe_load(file_descriptor)[yaml_config_field]


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--enable-benchmark", action="store_true", help="Enable benchmarking in tests")


def pytest_configure(config: Any) -> None:
    config.addinivalue_line("markers", "benchmark: mark test to run with benchmarking")
