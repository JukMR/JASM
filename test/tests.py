'Main test file'
import pytest
import yaml

import sys
sys.path.append('..')

from logging_config import logger
from run_regex import match


def load_test_configs(file_path):
    """Load test configurations from a YAML file."""
    with open(file_path, 'r', encoding='utf-8') as file_descriptor:
        return yaml.safe_load(file_descriptor)['test_configs']

def run_match_test(pattern_pathstr, assembly, expected_result):
    """Run a single match test."""
    result = match(pattern_pathstr=pattern_pathstr, assembly=assembly)
    assert result == expected_result


@pytest.mark.parametrize("config", load_test_configs('configuration.yml'),
                         ids=lambda config: config['yaml'])
def test(config):
    """Test function for all configurations in configuration.yml."""
    config_yaml = config['yaml']
    assembly = config['assembly']
    expected_result = config['expected']
    logger.info("Testing assembly: %s with pattern: %s", assembly, config_yaml)
    run_match_test(config_yaml, assembly, expected_result)
