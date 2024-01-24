# JASM Regex Generator

## Run

To run the project it is recommended to do `poetry shell` and execute the files from there.

## Parse an assembly file

python3 run_regex.py -p <pattern.yaml> -i -s <assembly_file.s>

## Parse a binary file

python3 run_regex.py -p <pattern.yaml> -i -b <binary_file.bin>

## Run tests

To run test you can, run `run_tests.sh` while inside `poetry shell`.

Another options is to simply call `pytest`

## Rules manual

A command can be either an instruction or an operand. The rules are as follows:

* `$and`: Matches all the command in the list

* `$or`: Matches any of the command in the list

* `$not`: Matches any command that is not in the list

* `$and_any_order`: Matches all the commands in the list in any order

* `@any`: Matches any command
