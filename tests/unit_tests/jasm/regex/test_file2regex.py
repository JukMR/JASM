# tests/unit_tests/test_file2regex.py
from pathlib import Path
from typing import Literal
from jasm.jasm_regex.file2regex import File2Regex
from jasm.global_definitions import DisassStyle
from jasm.global_definitions import JASMConfig


class ConcreteFile2Regex(File2Regex):  # type: ignore
    """Concrete implementation of File2Regex."""

    @staticmethod
    def load_file(file: str | Path) -> str:
        return f"Loaded {file}"

    def produce_regex(self) -> Literal["RegexPattern"]:
        return "RegexPattern"

    def load_config(self) -> None:
        JASMConfig.get_instance().load_config({"style": "att"})


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
    concrete_instance.load_config()
    assert JASMConfig.get_instance().get_info("assembly_style") == DisassStyle.att
