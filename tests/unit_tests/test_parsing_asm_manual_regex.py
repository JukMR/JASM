from jasm.stringify_asm.abstracts.abs_observer import Instruction
from jasm.stringify_asm.parsing_asm_manual_regex import LineParser


def test_lineparser_parse():
    line = "   1231:\t48 89 e5                \tmov    \t%rsp,%rbp  "
    parsed_inst = LineParser(line).parse()

    assert isinstance(parsed_inst, Instruction)
    operands = parsed_inst.operands
    assert operands == ["%rsp", "%rbp"]


def test_get_splitted_operands():
    assert LineParser.get_splitted_operands("%rsp,%rbp") == ["%rsp", "%rbp"]

    assert LineParser.get_splitted_operands("%rsp") == ["%rsp"]

    assert LineParser.get_splitted_operands("0x0(%rax,%rax,1)") == ["0x0(%rax,%rax,1)"]