from typing import Optional, Union

from jasm.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS, IGNORE_INST_ADDR,
    IGNORE_NAME_PREFIX, IGNORE_NAME_SUFFIX, SKIP_TO_END_OF_PATTERN_NODE, PatternNodeName, TimesType,
    JASMConfig, PartialMatchingConfig
)
from jasm.logging_config import logger
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode, PatternNodeData
from jasm.jasm_regex.tree_generators.pattern_node_implementations.time_type_builder import TimesTypeBuilder


class InstructionNodeHelper:
    @staticmethod
    def allow_matching_substring(key: PartialMatchingConfig) -> bool:
        # Retrieve the value of allow_matching_substrings from the singleton
        config = JASMConfig.get_instance()
        return not config.get_info(key)

    @staticmethod
    def get_pattern_node_name(
        name: Union[str, int],
        allow_matching_substrings: bool = ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
        name_prefix: str = IGNORE_NAME_PREFIX,
        name_suffix: str = IGNORE_NAME_SUFFIX,
    ) -> str:
        name_str = f"{name}"  # Convert to string explicitly
        if allow_matching_substrings:
            return f"{name_prefix}{name_str}{name_suffix}"
        return name_str + ","


class PatternNodeOperand(PatternNode):

    def __init__(self, pattern_node_data: PatternNodeData) -> None:
        super().__init__(pattern_node_data)
        self.helper = InstructionNodeHelper()

    @staticmethod
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

    @staticmethod
    def _process_hex_operand(hex_operand_elem: str) -> str:
        operand_elem = "0x" + hex_operand_elem.removesuffix("h")
        return operand_elem

    def get_regex(self) -> str:
        if self.children:
            logger.warning("Operand %s has children", self.name)
            raise ValueError(f"Operand should not have children - {self.name}")

        if self._is_hex_operand(self.name):
            # Match hex operand
            if not isinstance(self.name, str):
                raise TypeError("Operand name must be a string")
            return self._process_hex_operand(self.name)

        pattern_node_name = self.helper.get_pattern_node_name(
            self.name, self.helper.allow_matching_substring(PartialMatchingConfig.OperandsFullMatch)
        )
        return pattern_node_name


class PatternNodeMnemonic(PatternNode):

    def __init__(self, pattern_node_data: PatternNodeData) -> None:
        super().__init__(pattern_node_data)
        self.helper = InstructionNodeHelper()

    def get_regex(self) -> str:
        if not self.children:
            logger.debug("Mnemonic %s has no children", self.name)

        operands_regex: Optional[str] = self.get_operand_regex()
        times_regex: Optional[str] = self.get_min_max_regex()

        substr_flag = self.helper.allow_matching_substring(PartialMatchingConfig.MnemonicsFullMatch)
        if times_regex:
            return self._form_regex_with_time(
                operands_regex=operands_regex, times_regex=times_regex,
                allow_matching_substrings=substr_flag
            )
        return self._form_regex_without_time(
            operands_regex=operands_regex, allow_matching_substrings=substr_flag
        )

    def get_operand_regex(self) -> Optional[str]:
        if not self.children:
            return None

        return "".join(operand.get_regex() for operand in self.children)

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None

        return TimesTypeBuilder().get_min_max_regex(times=self.times)  # type: ignore

    def _form_regex_with_time(
        self, operands_regex: Optional[str], times_regex: str,
        allow_matching_substrings: bool = True
    ) -> str:
        # Add prefix and suffix to name to allow matching only substring
        pattern_node_name = self.helper.get_pattern_node_name(self.name, allow_matching_substrings)

        if operands_regex:
            return f"(?:{IGNORE_INST_ADDR}(?:{pattern_node_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"
        return f"(?:{IGNORE_INST_ADDR}(?:{pattern_node_name}{SKIP_TO_END_OF_PATTERN_NODE})){times_regex}"

    def _form_regex_without_time(
        self, operands_regex: Optional[str], allow_matching_substrings: bool = True
    ) -> str:
        pattern_node_name = self.helper.get_pattern_node_name(self.name, allow_matching_substrings)

        if operands_regex:
            return f"{IGNORE_INST_ADDR}(?:{pattern_node_name}{operands_regex}{SKIP_TO_END_OF_PATTERN_NODE})"
        return f"{IGNORE_INST_ADDR}(?:{pattern_node_name}{SKIP_TO_END_OF_PATTERN_NODE})"
