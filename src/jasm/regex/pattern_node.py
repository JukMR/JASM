"PatternNode definition file"

from itertools import permutations
from typing import List, Optional

from jasm.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    IGNORE_INST_ADDR,
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    SKIP_TO_END_OF_PATTERNNODE,
    ASTERISK_WITH_LIMIT,
    PatternNodeTypes,
    TimeType,
    dict_node,
)
from jasm.regex.deref_classes import DerefObject, DerefObjectBuilder


def get_pattern_node_name(
    name: str | int,
    allow_matching_substrings: bool = ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    name_prefix: str = IGNORE_NAME_PREFIX,
    name_suffix: str = IGNORE_NAME_SUFFIX,
) -> str | int:
    if name == "@any":
        name = rf"[^, ]{ASTERISK_WITH_LIMIT}"  # Set a limit of 10 characters for the name for reducing regex complexity
    if allow_matching_substrings:
        return f"{name_prefix}{name}{name_suffix}"
    return name


class PatternNode:
    def __init__(
        self,
        pattern_node_dict: dict_node,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["PatternNode"]],
        pattern_node_type: Optional[PatternNodeTypes],
        parent: Optional["PatternNode"],
    ) -> None:
        """
        Initialize a Command object.

        :param pattern_node_dict: A dictionary representing the pattern_nod structure.
        :param name: The name of the pattern_nod.
        :param times: Repeating information for the pattern_nod execution.
        :param children: Sub-pattern_nods or child pattern_nods.
        :param pattern_nod_type: The type of the pattern_nod (mnemonic, operand, etc.).
        :param parent: The parent pattern_nod, if any.
        """
        self.pattern_node_dict = pattern_node_dict
        self.name = name
        self.times = times
        self.children = children
        self.pattern_node_type = pattern_node_type
        self.parent = parent

    def get_regex(self, pattern_node: "PatternNode") -> str:
        if pattern_node.pattern_node_type in [PatternNodeTypes.mnemonic, PatternNodeTypes.operand]:
            return self.process_leaf(pattern_node)

        if pattern_node.pattern_node_type == PatternNodeTypes.deref_property:
            return self.process_deref_child(pattern_node)

        if pattern_node.pattern_node_type == PatternNodeTypes.times:
            return ""
        return self.process_branch(pattern_node)

    def process_leaf(self, pattern: "PatternNode") -> str:
        name = pattern.name
        children = pattern.children
        times = pattern.times
        if not children:
            if pattern.pattern_node_type == PatternNodeTypes.operand:
                # Is an operand
                return str(self.sanitize_operand_name(name))
            # Is a mnemonic with no operands
            print(f"Found a mnemonic with no operands in yaml rule: {pattern.name}")

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

    def process_branch(self, pattern_node: "PatternNode") -> str:
        child_regexes = self.process_children(pattern_node)
        times_regex: Optional[str] = global_get_min_max_regex(times=pattern_node.times)
        return BranchProcessor().process_pattern_node(
            pattern_node.name, child_regexes, times_regex, pattern_node.pattern_node_dict
        )

    def process_children(self, pattern_node: "PatternNode") -> List[str]:
        if pattern_node.children:
            return [self.get_regex(child) for child in pattern_node.children]
        raise ValueError("Children list is empty")

    def process_deref_child(self, pattern_node: "PatternNode") -> str | int:
        assert isinstance(pattern_node.pattern_node_dict, tuple)
        result = pattern_node.pattern_node_dict[1]
        assert isinstance(result, str | int)
        return result


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

        return "".join(operand.get_regex(operand) for operand in self.operands)

    def get_min_max_regex(self) -> Optional[str]:
        if not self.times:
            return None
        return global_get_min_max_regex(times=self.times)

    def _form_regex_with_time(self, operands_regex: Optional[str], times_regex: str) -> str:
        # Add prefix and suffix to name to allow matching only substring
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return (
                f"(({IGNORE_INST_ADDR}{pattern_nod_name}({operands_regex}){SKIP_TO_END_OF_PATTERNNODE}){times_regex})"
            )
        return f"(({IGNORE_INST_ADDR}{pattern_nod_name}{SKIP_TO_END_OF_PATTERNNODE}){times_regex})"

    def _form_regex_without_time(self, operands_regex: Optional[str]) -> str:
        pattern_nod_name = get_pattern_node_name(self.name)

        if operands_regex:
            return f"({IGNORE_INST_ADDR}{pattern_nod_name}{operands_regex}{SKIP_TO_END_OF_PATTERNNODE})"
        return f"({IGNORE_INST_ADDR}{pattern_nod_name}{SKIP_TO_END_OF_PATTERNNODE})"


class BranchProcessor:
    def process_pattern_node(
        self, pattern_nod_name: str | int, child_regexes: List[str], times_regex: Optional[str], pattern_node_dict: dict
    ) -> str:
        """
        Process a pattern_node based on its name and child regexes.

        :param pattern_node_name: The name of the pattern_node.
        :param child_regexes: List of regexes from child pattern_nodes.
        :param times_regex: The regex string for repeating the match.
        :return: The processed pattern_node regex.
        """
        assert isinstance(pattern_node_dict, dict)
        match pattern_nod_name:
            # Match case where pattern_nod.name is and or pattern

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
            case "$deref":
                assert isinstance(pattern_node_dict, dict)
                deref_object = DerefObjectBuilder(pattern_node_dict).build()
                return self.process_deref(deref_object, times_regex=times_regex)
            case _:
                raise ValueError("Unknown pattern_nod type")

    @staticmethod
    def process_and(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"({''.join(child_regexes) + SKIP_TO_END_OF_PATTERNNODE}){times_regex}"
        return f"({''.join(child_regexes)})"

    def process_or(self, child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"({self.join_instructions(child_regexes)}){times_regex}"
        return f"({self.join_instructions(child_regexes)})"

    @staticmethod
    def process_not(child_regexes: List[str], times_regex: Optional[str]) -> str:
        if times_regex:
            return f"((?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERNNODE}){times_regex}"
        return f"((?!{''.join(child_regexes)}){SKIP_TO_END_OF_PATTERNNODE})"

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

    def process_deref(self, deref_object: DerefObject, times_regex: Optional[str]) -> str:
        deref_regex = deref_object.get_regex()
        if times_regex:
            return f"({deref_regex},){times_regex}"
        return f"{deref_regex},"

    @staticmethod
    def generate_any_order_permutation(child_regexes: List[str]) -> List[List[str]]:
        # Generate all the permutation of this list
        return [list(permutation) for permutation in permutations(child_regexes)]

    @staticmethod
    def join_instructions(inst_list: List[str]) -> str:
        "Join instructions from list using operand to generate regex"

        assert inst_list, "There are no instructions to join"

        regex_instructions = [f"({elem})" for elem in inst_list]

        joined_by_bar_instructions = "|".join(regex_instructions)

        return joined_by_bar_instructions


def global_get_min_max_regex(times: TimeType) -> Optional[str]:
    if times.min_times == 1 and times.max_times == 1:
        return None
    if times.min_times == times.max_times:
        return f"{{{times.min_times}}}"
    return f"{{{times.min_times},{times.max_times}}}"
