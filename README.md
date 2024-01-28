# JASM Regex Generator

## Run

To run the project it is recommended to do `poetry shell` and execute the files from there.

## Parse an assembly file

python3 main.py -p <pattern.yaml> -s <assembly_file.s>

## Parse a binary file

python3 main.py -p <pattern.yaml> -b <binary_file.bin>

## Help

To see the help run `python3 main.py -h` or `python3 main.py --help`

## Run tests

To run test you can,

* Run `sh run_tests.sh` while inside `poetry shell`.

* Another options is to simply call `pytest`

## Manual Rules

The rules for using in the patterns are as follows:

* `$and`: Matches all the command in the list

* `$or`: Matches any of the command in the list

* `$not`: Matches any command that is not in the list

* `$and_any_order`: Matches all the commands in the list in any order

* `@any`: Matches any command

* `$deref`: Used for dereferencing a register

NOTE: the `$deref` commands require the following syntax, using the example below:

```
    - $deref:
        main_reg: "%rax"
        constant_offset: "0x0"
        register_multiplier: "%rax"
        constant_multiplier: 1


```

This would be transforming the objdump syntax into golbolt one:

k(a,b,c) -> [a+b*c+k]
objdump syntax -> jasm/golbolt syntax

where:

* `main_reg: a`

* `constant_multiplier: b`

* `register_multiplier: c`

* `constant_offset: k`

So the example would match a command like `nopw 0x0(%rax,%rax,1)` turning it to `[%rax+%rax*1+0x0]`
