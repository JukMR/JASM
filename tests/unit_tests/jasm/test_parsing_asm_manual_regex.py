from jasm.global_definitions import Instruction
from jasm.stringify_asm.implementations.gnu_objdump.asm_manual_parser_w_regex import LineParser


def test_lineparser_parse() -> None:
    line = "   1231:\t48 89 e5                \tmov    \t%rsp,%rbp  "
    parsed_inst = LineParser(line).parse()

    assert isinstance(parsed_inst, Instruction)
    operands = parsed_inst.operands
    assert operands == ["%rsp", "%rbp"]


def test_get_splitted_operands() -> None:
    assert LineParser.get_splitted_operands("%rsp,%rbp") == ["%rsp", "%rbp"]

    assert LineParser.get_splitted_operands("%rsp") == ["%rsp"]

    assert LineParser.get_splitted_operands("0x0(%rax,%rax,1)") == ["0x0(%rax,%rax,1)"]
