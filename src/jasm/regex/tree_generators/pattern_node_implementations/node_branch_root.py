from itertools import permutations
from typing import List, Optional

from jasm.global_definitions import SKIP_TO_END_OF_PATTERN_NODE
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.time_type_builder import TimesTypeBuilder


class PatternNodeTimes(PatternNode):

    def get_regex(self) -> str:
        return ""


class PatternNodeBranchRoot(PatternNode):

    def get_regex(self) -> str:
        return self.process_branch()

    def process_branch(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimesTypeBuilder().get_min_max_regex(times=self.times)
        return _BranchProcessor().process_pattern_node(
            parent=self, child_regexes=child_regexes, times_regex=times_regex
        )

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class PatternNodeBranch(PatternNodeBranchRoot):
    pass


class PatternNodeRoot(PatternNodeBranchRoot):
    """
    This is the case of the root node $and
    """


class PatternNodeNode(PatternNodeBranchRoot):
    pass


class _BranchProcessor:
    def process_pattern_node(
        self,
        parent: PatternNode,
        child_regexes: List[str],
        times_regex: Optional[str],
    ) -> str:
        """
        Process a pattern_node based on its name and child regexes.

        :param pattern_node_name: The name of the pattern_node.
        :param child_regexes: List of regexes from child pattern_nodes.
        :param times_regex: The regex string for repeating the match.
        :return: The processed pattern_node regex.
        """
        match parent.name:
            # Match case where pattern_node.name is and or pattern

            case "$and":
                return self.process_and(child_regexes, times_regex=times_regex)
            case "$or":
                return self.process_or(child_regexes, times_regex=times_regex)
            case "$not":
                return self.process_not(child_regexes, times_regex=times_regex)
            # case "$perm":
            #     return self.process_perm(child_regexes, times_regex=times_regex)
            case "$and_any_order":
                return self.process_and_any_order(child_regexes, times_regex=times_regex)
            case _:
                raise ValueError("Unknown pattern_node type")

    @staticmethod
    def process_and(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{''.join(child_regexes) + SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:{''.join(child_regexes)})"

    def process_or(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:{self.join_or_instructions(child_regexes)}){times_regex}"
        return f"(?:{self.join_or_instructions(child_regexes)})"

    @staticmethod
    def process_not(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE}){times_regex}"
        return f"(?:(?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERN_NODE})"

    def process_and_any_order(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        full_all_against_all_regex: List[List[str]] = self.generate_any_order_permutation(child_regexes)

        regex_list: List[str] = []
        for list_regex in full_all_against_all_regex:
            regex_list.append(self.process_and(child_regexes=list_regex, times_regex=None))

        return self.process_or(regex_list, times_regex)

    @staticmethod
    def generate_any_order_permutation(child_regexes: List[str]) -> List[List[str]]:
        # Generate all the permutation of this list
        return [list(permutation) for permutation in permutations(child_regexes)]

    @staticmethod
    def join_or_instructions(inst_list: List[str]) -> str:
        "Join instructions from list using operand to generate regex"

        assert inst_list, "There are no instructions to join"

        regex_instructions = [f"(?:{elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions
