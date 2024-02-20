# tests/unit_tests/test_file2regex.py
from jasm.regex.file2regex import File2Regex
from jasm.global_definitions import DisassStyle


class ConcreteFile2Regex(File2Regex):
    @staticmethod
    def load_file(file) -> str:
        return f"Loaded {file}"

    def produce_regex(self):
        return "RegexPattern"

    def get_assembly_style(self):
        return DisassStyle.att


def test_load_file():
    assert ConcreteFile2Regex.load_file("testfile.txt") == "Loaded testfile.txt"


def test_produce_regex():
    concrete_instance = ConcreteFile2Regex()
    assert concrete_instance.produce_regex() == "RegexPattern"


def test_get_assembly_style():
    concrete_instance = ConcreteFile2Regex()
    assert concrete_instance.get_assembly_style() == DisassStyle.att
