import sys
sys.path.append('..')

import yaml

from run_regex import match

def test_all_configs():
    with open('configuration.yml', 'r') as fd:
        loaded_yaml = yaml.safe_load(fd)

    for config in loaded_yaml['test_configs']:
        config_yaml = config['yaml']
        assembly = config['assembly']
        expected_result = config['expected']
        assert match(pattern_pathStr=config_yaml, assembly=assembly) == expected_result