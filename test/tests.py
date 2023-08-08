import sys
sys.path.append('..')

from run_regex import match

def test_8_calls():
    assert match(yaml_pathStr='yaml/8_calls.yml', binary='binary/binary_data.s', debug=False) == True


def test_9_calls():
    assert match(yaml_pathStr='yaml/9_calls.yml', binary='binary/binary_data.s', debug=False) == False