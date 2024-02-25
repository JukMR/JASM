from unittest.mock import patch, MagicMock
import pytest
from jasm.regex.macro_expander.macro_expander import MacroExpander


@pytest.fixture
def macro_expander():
    return MacroExpander()


def test_resolve_all_macros(macro_expander):
    macros = [
        {"name": "MACRO1", "pattern": "replacement1"},
        {"name": "MACRO2", "pattern": "replacement2"},
    ]
    tree = "test MACRO1 and MACRO2"

    with patch.object(
        macro_expander, "_resolve_macro", side_effect=lambda macro, tree: tree.replace(macro["name"], macro["pattern"])
    ) as mock_resolve_macro:
        result = macro_expander.resolve_all_macros(macros, tree)
        assert result == "test replacement1 and replacement2"
        assert mock_resolve_macro.call_count == len(macros)
