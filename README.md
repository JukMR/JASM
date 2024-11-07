# JASM Regex Generator

## Run

### Setup

It's recommended to use a virtual environment to run the project. To do so, follow these steps:

``` bash
poetry shell
```

Install the project dependencies:

```bash

    poetry install
```

Check if the project is working:

```bash

    jasm --help
```

## Parse an assembly file

```bash
jasm -p <pattern.yaml> -s <assembly_file.s>
```

## Parse a binary file

```bash
jasm -p <pattern.yaml> -b <binary_file.bin>
```

## Use of macros

You can also specify a macro file which will be used as the macros definitions. Examples of these files can be seen in `tests/macros/`.

```bash
jasm -p <pattern.yaml> -s <assembly_file.s> --macros <macro_file.yaml>
```

The macro `tests/macros/jasm_macros.yaml` has the `@any` macro for example, which is used to match with any mnemonic or any operand.

### Macro Naming convention

Macro names must start with the "@" identifier. Here is an example:

```yaml
macros:
  - name: "@macro_1"
    pattern: "replace_1"
```

## Help

To see the help run `jasm -h` or `jasm --help`

## Run tests

To run test you just call `pytest`

## Manual Rules

The rules for using in the patterns are as follows:

* `$and`: Matches all the command in the list

* `$or`: Matches any of the command in the list

* `$not`: Matches any command that is not in the list

* `$and_any_order`: Matches all the commands in the list in any order

* `@any`: Matches any command

* `$deref`: Used for dereferencing a register

NOTE: the `$deref` commands require the following syntax, using the example below:

```yaml
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

## Special registry capture groups

The x86 registers are the following:

![x86 registers](x86_registers.png)

we support the following convention for using special register captures.

Use the capture group special names for capturing the registers:

* `&genreg`

* `&indreg`

* `&stackreg`

* `&basereg`

And these suffix for accessing the specific parts of the registers:

* `.64`

* `.32`

* `.16`

* `.8H`

* `.8L`

So for example:

* if you want to capture the `rax` register you can use `&genreg.64` and it will capture the `rax` register.
* if you want to capture the `eax` register you can use `&genreg.32` and it will capture the `eax` register.
* if you want to capture the `ax` register you can use `&genreg.16` and it will capture the `ax` register.
* if you want to capture the `ah` register you can use `&genreg.8H` and it will capture the `ah` register.
* if you want to capture the `al` register you can use `&genreg.8L` and it will capture the `al` register.

## Configuration

Global configuration for a JASM rule can be specified in the configuration section. The current options for configuration are:

* style: Specifies the assembly style. Possible values include att for AT&T syntax.
* mnemonics-full-match: A boolean value indicating whether the mnemonics should be matched fully.
* operands-full-match: A boolean value indicating whether the operands should be matched fully.
* sections: Specifies the sections to disassemble given a binary.
Example:

```yaml
config:
  style: att
  mnemonics-full-match: true
  operands-full-match: true
  sections:
    - ".plt"
    - ".plt.got"
```

## Troubleshooting

### Cannot install profiler-measure

If poetry is failing to install this dependency, it may be because it cannot access gitlab credentials correctly.
Create a `.netrc` file under your home directory with the following content:

```
machine gitlab.com login <eclypsium_email> password <gitlab_user_token>
```

This should allow poetry to access gitlab repositories and look for this package.
