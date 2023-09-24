# JASM Regex Generator

## Run

To run the project it is recommended to do `poetry shell` and execute the files from there.

## Parse an assembly file

python3 run_regex.py -p <pattern.yaml> -s <assembly_file.s>

## Parse a binary file

python3 run_regex.py -p <pattern.yaml> -b <binary_file.bin>

## Run tests

To run test you can, run `run_tests.sh` while inside `poetry shell`.

Another options is to simply call `pytest`
