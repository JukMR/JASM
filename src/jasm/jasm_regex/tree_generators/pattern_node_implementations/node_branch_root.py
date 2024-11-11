from abc import abstractmethod
from itertools import permutations
from typing import List, Optional, Generator

from jasm.global_definitions import SKIP_TO_END_OF_PATTERN_NODE
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.jasm_regex.tree_generators.pattern_node_implementations.time_type_builder import TimesTypeBuilder


class PatternNodeTimes(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return ""


class LogicalOperationBaseNode(PatternNode):

    def get_regex(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimesTypeBuilder().get_min_max_regex(times=self.times)
        return self._make_main_regex(child_regexes, times_regex)

    @abstractmethod
    def _make_main_regex(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        pass

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class NodeAnd(LogicalOperationBaseNode):

    def _make_main_regex(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{''.join(child_regexes) + SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:{''.join(child_regexes)})"


class NodeOr(LogicalOperationBaseNode):

    def _make_main_regex(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{self.join_or_instructions(child_regexes)}){times_regex}"
        return f"(?:{self.join_or_instructions(child_regexes)})"

    @staticmethod
    def join_or_instructions(inst_list: List[str]) -> str:
        "Join instructions from list using operand to generate regex"

        if not inst_list:
            raise ValueError("There are no instructions to join")

        regex_instructions = [f"(?:{elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions


class NodeNot(LogicalOperationBaseNode):

    def _make_main_regex(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE})"


class NodeAndAnyOrder(NodeAnd):

    def _make_main_regex(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        full_all_against_all_regex: List[List[str]
                                         ] = self.generate_any_order_permutation(child_regexes)

        regex_list: List[str] = []
        for list_regex in full_all_against_all_regex:
            regex_list.append(super()._make_main_regex(list_regex, None))

        return self.join_or_instructions(regex_list, times_regex)

    @staticmethod
    def generate_any_order_permutation(child_regexes: List[str]) -> List[List[str]]:
        # Generate all the permutation of this list
        return [list(permutation) for permutation in permutations(child_regexes)]

    @staticmethod
    def join_or_instructions(inst_list: List[str], times_regex: Optional[str]) -> str:
        "Join instructions from list using operand to generate regex"

        if not inst_list:
            raise ValueError("There are no instructions to join")

        regex_instructions = [f"(?:{elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        if times_regex:
            return f"(?:{joined_by_bar_instructions}){times_regex}"
        return f"(?:{joined_by_bar_instructions})"
