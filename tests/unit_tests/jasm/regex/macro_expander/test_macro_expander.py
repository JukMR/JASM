from unittest.mock import patch
import pytest
from jasm.jasm_regex.macro_expander.macro_expander import MacroExpander

@pytest.fixture
def macro_expander() -> MacroExpander:
    return MacroExpander()

def test_resolve_all_macros(macro_expander: MacroExpander) -> None:
    macros = [
        {"name": "@MACRO1", "pattern": "replacement1"},
        {"name": "@MACRO2", "pattern": "replacement2"},
    ]
    tree = "test @MACRO1 and @MACRO2"

    with patch.object(
        macro_expander, "_resolve_macro", side_effect=lambda macro, tree, rule_macros: tree.replace(macro["name"], macro["pattern"])
    ) as mock_resolve_macro:
        result = macro_expander.resolve_all_macros(macros, tree)
        assert result == "test replacement1 and replacement2"
        assert mock_resolve_macro.call_count == len(macros)


def test_unresolved_macro(macro_expander: MacroExpander) -> None:
    macros = [
        {"name": "@MACRO1", "pattern": "replacement1"},
        {"name": "@MACRO2", "pattern": "replacement2"},
    ]
    tree = "@MACRO3"

    with pytest.raises(ValueError, match="The following macros are not defined: {'@MACRO3'}"):
        macro_expander.resolve_all_macros(macros, tree)
