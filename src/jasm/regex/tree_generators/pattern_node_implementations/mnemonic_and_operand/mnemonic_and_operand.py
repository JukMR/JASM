from typing import List, Optional

from jasm.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    ASTERISK_WITH_LIMIT,
    IGNORE_INST_ADDR,
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    SKIP_TO_END_OF_PATTERN_NODE,
    PatternNodeName,
    TimesType,
)
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.time_type_builder import TimesTypeBuilder


def get_pattern_node_name(
    name: str | int,
    allow_matching_substrings: bool = ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    name_prefix: str = IGNORE_NAME_PREFIX,
    name_suffix: str = IGNORE_NAME_SUFFIX,
) -> str | int:
    if name == "@any":
        name = (
            rf"[^, ]{ASTERISK_WITH_LIMIT}"  # Set a limit of 1000 characters for the name for reducing regex complexity
        )
    if allow_matching_substrings:
        return f"{name_prefix}{name}{name_suffix}"
    return name


class _PatternNodeMnemonicOrOperandBuilder(PatternNode):  # type: ignore
    """This class is used to process PatternNodeMnemonic and PatternNodeOperand classes."""

    def get_regex(self) -> str:
        return self.process_leaf()

    def process_leaf(self) -> str:
        name = self.name
        children = self.children
        times = self.times

        # Leaf is operand
        if not children and isinstance(self, PatternNodeOperand):
            # Is an operand
            return str(self._sanitize_operand_name(name))
        # Is a mnemonic with no operands
        print(f"Found a mnemonic with no operands in yaml rule: {self.name}")

        assert isinstance(children, List) or (not children), "Children must be a list or None"
        # This line shouldn't be necessary but the linter complains children could be dict
        assert not isinstance(children, dict), "Children must be a list or None"
        return _RegexWithOperandsBuilder(name=name, operands=children, times=times).generate_regex()

    def _sanitize_operand_name(self, name: PatternNodeName) -> PatternNodeName:
        def _is_hex_operand(name: PatternNodeName) -> bool:
            if isinstance(name, int):
                return False
            if name.endswith("h"):
                tmp = name.removesuffix("h")
                try:
                    int(tmp, base=16)
                    return True
                except ValueError:
                    return False
            return False

        if _is_hex_operand(name):

            def _process_hex_operand(hex_operand_elem: str) -> str:
                operand_elem = "0x" + hex_operand_elem.removesuffix("h")
                return operand_elem

            # Match hex operand
            assert isinstance(name, str), "Operand name must be a string"
            return _process_hex_operand(name)

        pattern_nod_name = get_pattern_node_name(name)
        return pattern_nod_name


class PatternNodeMnemonic(_PatternNodeMnemonicOrOperandBuilder):
    pass


class PatternNodeOperand(_PatternNodeMnemonicOrOperandBuilder):
    pass


class _RegexWithOperandsBuilder:
    def __init__(
        self, name: PatternNodeName, operands: Optional[List[PatternNode]], times: Optional[TimesType]
    ) -> None:
        self.name = name
        self.operands = operands
        self.times = times

    def generate_regex(self) -> str:
        operands_regex: Optional[str] = self.get_operand_regex()
        times_regex: Optional[str] = self.get_min_max_regex()

        if times_regex:
            return self._form_regex_with_time(operands_regex=operands_regex, times_regex=times_regex)
        return self._form_regex_without_time(operands_regex=operands_regex)

    def get_operand_regex(self) -> Optional[str]:
        if not self.operands:
            return None

        return "".join(operand.get_regex() for operand in self.operands)

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None

        result: Optional[str] = TimesTypeBuilder().get_min_max_regex(times=self.times)
        return result

    def _form_regex_with_time(self, operands_regex: Optional[str], times_regex: str) -> str:
        # Add prefix and suffix to name to allow matching only substring
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return f"(?:{IGNORE_INST_ADDR}(?:{pattern_nod_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"
        return f"(?:{IGNORE_INST_ADDR}(?:{pattern_nod_name}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"

    def _form_regex_without_time(self, operands_regex: Optional[str]) -> str:
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return f"{IGNORE_INST_ADDR}(?:{pattern_nod_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})"
        return f"{IGNORE_INST_ADDR}(?:{pattern_nod_name}{SKIP_TO_END_OF_PATTERN_NODE})"
