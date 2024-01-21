from pathlib import Path

from src.regex.yaml2regex import Yaml2Regex


def load_regex_rule_no_macro(yamls_directory: Path) -> dict:
    file_path = yamls_directory / "include_and_include_list_with_macros_manual.yaml"
    file_pathstr = str(file_path)
    return Yaml2Regex(pattern_pathstr=file_pathstr).get_pattern()


def load_regex_rule_with_macro(yamls_directory: Path) -> dict:
    file_path = yamls_directory / "include_and_include_list_with_macros.yaml"
    file_pathstr = str(file_path)
    return Yaml2Regex(pattern_pathstr=file_pathstr).get_pattern()


def test_macro_feature() -> None:
    yamls_directory = Path("tests/yamls")

    if not yamls_directory.exists():
        raise FileNotFoundError("The yamls directory does not exists")

    regex_no_macro = load_regex_rule_no_macro(yamls_directory)
    regex_with_macro = load_regex_rule_with_macro(yamls_directory)
    assert regex_no_macro == regex_with_macro


if __name__ == "__main__":
    test_macro_feature()
