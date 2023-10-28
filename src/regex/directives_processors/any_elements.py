from dataclasses import dataclass
from re import S
from typing import List

from src.global_definitions import IGNORE_INST_ADDR, SKIP_TO_END_OF_COMMAND, SKIP_TO_END_OF_OPERAND


@dataclass
class RuleElement:
    mnemonic: str
    operands: List[str]

    def get_regex(self) -> str:
        return f"{self.get_mnemonic_regex()},{self.get_operand_regex()}"

    def get_mnemonic_regex(self) -> str:
        return f"{IGNORE_INST_ADDR}{self.mnemonic}"

    def get_operand_regex(self) -> str:
        def process_operand(operand: str | int) -> str:
            if isinstance(operand, int):
                return str(operand) + SKIP_TO_END_OF_OPERAND
            if operand == "$any":
                return SKIP_TO_END_OF_COMMAND
            return operand + SKIP_TO_END_OF_OPERAND

        operands_regex = "".join(process_operand(operand) for operand in self.operands)
        return operands_regex
