import sys
sys.path.append('..')

import yaml

from run_regex import match

def test_all_configs():
    with open('configuration.yml', 'r') as fd:
        loaded_yaml = yaml.safe_load(fd)

    for config in loaded_yaml['test_configs']:
        config_yaml = config['yaml']
        binary = config['binary']
        expected_result = config['expected']
        assert match(yaml_pathStr=config_yaml, binary=binary) == expected_result

def test_8_calls():
    assert match(yaml_pathStr='yaml/9_calls.yml', binary='binary/binary_data.s', debug=False) == True


def test_9_calls():
    assert match(yaml_pathStr='yaml/10_calls.yml', binary='binary/binary_data.s', debug=False) == False