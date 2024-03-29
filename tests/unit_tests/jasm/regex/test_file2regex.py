# tests/unit_tests/test_file2regex.py
from pathlib import Path
from typing import Literal
from jasm.regex.file2regex import File2Regex
from jasm.global_definitions import DisassStyle


class ConcreteFile2Regex(File2Regex):  # type: ignore
    """Concrete implementation of File2Regex."""

    @staticmethod
    def load_file(file: str | Path) -> str:
        return f"Loaded {file}"

    def produce_regex(self) -> Literal["RegexPattern"]:
        return "RegexPattern"

    def get_assembly_style(self) -> DisassStyle:
        return DisassStyle.att


def test_load_file() -> None:
    """Test load_file method."""
    assert ConcreteFile2Regex.load_file("testfile.txt") == "Loaded testfile.txt"


def test_produce_regex() -> None:
    """Test produce_regex method."""
    concrete_instance = ConcreteFile2Regex()
    assert concrete_instance.produce_regex() == "RegexPattern"


def test_get_assembly_style() -> None:
    """Test get_assembly_style method."""
    concrete_instance = ConcreteFile2Regex()
    assert concrete_instance.get_assembly_style() == DisassStyle.att
