# tests/unit_tests/test_file2regex.py
from src.regex.file2regex import File2Regex


class ConcreteFile2Regex(File2Regex):
    @staticmethod
    def load_file(file) -> str:
        return f"Loaded {file}"

    def produce_regex(self):
        return "RegexPattern"


def test_load_file():
    assert ConcreteFile2Regex.load_file("testfile.txt") == "Loaded testfile.txt"


def test_produce_regex():
    concrete_instance = ConcreteFile2Regex()
    assert concrete_instance.produce_regex() == "RegexPattern"
