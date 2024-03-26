from itertools import permutations
from typing import List, Optional

from jasm.global_definitions import (
    IGNORE_INST_ADDR,
    SKIP_TO_END_OF_PATTERN_NODE,
    TimeType,
)
from jasm.regex.tree_generators.pattern_node import PatternNode, get_pattern_node_name
from jasm.regex.tree_generators.pattern_node_implementations.time_type_builder import TimeTypeBuilder


class PatternNodeTimes(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return ""


class _PatternNodeMnemonicOrOperandProcessor(PatternNode):
    """This class is used to process PatternNodeMnemonic and PatternNodeOperand classes."""

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_leaf()

    def process_leaf(self) -> str:
        name = self.name
        children = self.children
        times = self.times

        # Leaf is operand
        if not children and isinstance(self, PatternNodeOperand):
            # Is an operand
            return str(self.sanitize_operand_name(name))
        # Is a mnemonic with no operands
        print(f"Found a mnemonic with no operands in yaml rule: {self.name}")

        assert isinstance(children, List) or (not children), "Children must be a list or None"
        # This line shouldn't be necessary but the linter complains children could be dict
        assert not isinstance(children, dict), "Children must be a list or None"
        return RegexWithOperandsCreator(name=name, operands=children, times=times).generate_regex()

    def sanitize_operand_name(self, name: str | int) -> str | int:
        def _is_hex_operand(name: str | int) -> bool:
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


class PatternNodeMnemonic(_PatternNodeMnemonicOrOperandProcessor):
    pass


class PatternNodeOperand(_PatternNodeMnemonicOrOperandProcessor):
    pass


class PatternNodeBranchNodeRoot(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            pattern_node_dict=pattern_node.pattern_node_dict,
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            root_node=pattern_node.root_node,
        )

    def get_regex(self) -> str:
        return self.process_branch()

    def process_branch(self) -> str:
        child_regexes = self.process_children()
        times_regex: Optional[str] = TimeTypeBuilder().get_min_max_regex(times=self.times)
        return BranchProcessor().process_pattern_node(parent=self, child_regexes=child_regexes, times_regex=times_regex)

    def process_children(self) -> List[str]:
        if self.children:
            return [child.get_regex() for child in self.children]
        raise ValueError("Children list is empty")


class PatternNodeBranch(PatternNodeBranchNodeRoot):
    pass


class PatternNodeRoot(PatternNodeBranchNodeRoot):
    """
    This is the case of the root node $and
    In here we will be save the state of the capture group references
    """


class PatternNodeNode(PatternNodeBranchNodeRoot):
    pass


class BranchProcessor:
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

    # @staticmethod
    # def process_perm(child_regexes: List[str], times_regex: Optional[str]) -> str:
    #     # TODO: implement this
    #     return ""

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


class RegexWithOperandsCreator:
    def __init__(self, name: str | int, operands: Optional[List[PatternNode]], times: Optional[TimeType]) -> None:
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
        return TimeTypeBuilder().get_min_max_regex(times=self.times)

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
