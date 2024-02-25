from pathlib import Path

from jasm.regex.macro_expander.macro_expander import PatternTree
from jasm.regex.yaml2regex import Yaml2Regex


def load_regex_rule_no_macro(yamls_directory: Path) -> PatternTree:
    file_path = yamls_directory / "include_and_include_list_with_macros_manual.yaml"
    file_pathstr = str(file_path)
    return Yaml2Regex(pattern_pathstr=file_pathstr)._get_pattern()  # pylint: disable=protected-access


def load_regex_rule_with_macro(yamls_directory: Path) -> PatternTree:
    file_path = yamls_directory / "include_and_include_list_with_macros.yaml"
    file_pathstr = str(file_path)
    return Yaml2Regex(pattern_pathstr=file_pathstr)._get_pattern()  # pylint: disable=protected-access


def test_macro_feature() -> None:
    yamls_directory = Path("tests/yamls")

    if not yamls_directory.exists():
        raise FileNotFoundError("The yamls directory does not exists")

    regex_no_macro = load_regex_rule_no_macro(yamls_directory)
    regex_with_macro = load_regex_rule_with_macro(yamls_directory)
    assert regex_no_macro == regex_with_macro


def test_macro_from_args() -> None:
    test_directory = Path("tests")

    yamls_directory = test_directory / "yamls"
    yaml_file = yamls_directory / "macros_from_terminal.yaml"

    macros_directory = test_directory / "macros"
    macro_1_filepath = macros_directory / "macro_1.yaml"
    macro_2_filepath = macros_directory / "macro_2.yaml"

    regex = Yaml2Regex(
        pattern_pathstr=str(yaml_file), macros_from_terminal=[str(macro_1_filepath), str(macro_2_filepath)]
    ).produce_regex()  # pylint: disable=protected-access

    assert (
        regex
        == r"(?:[\dabcedf]+::(?:[^,|]{0,1000}replace_1[^,|]{0,1000},[^|]{0,1000}\|)[\dabcedf]+::(?:[^,|]{0,1000}replace_2[^,|]{0,1000},[^|]{0,1000}\|)[\dabcedf]+::(?:[^,|]{0,1000}replace_3[^,|]{0,1000},[^|]{0,1000}\|)[\dabcedf]+::(?:[^,|]{0,1000}replace_4[^,|]{0,1000},[^|]{0,1000}\|))"
    )
