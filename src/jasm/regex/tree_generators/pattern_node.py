"PatternNode definition file"

from abc import ABC, abstractmethod
from typing import List, Optional

from jasm.global_definitions import (
    ALLOW_MATCHING_SUBSTRINGS_IN_NAMES_AND_OPERANDS,
    ASTERISK_WITH_LIMIT,
    IGNORE_NAME_PREFIX,
    IGNORE_NAME_SUFFIX,
    DictNode,
    TimeType,
)


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


class PatternNode(ABC):
    def __init__(
        self,
        pattern_node_dict: DictNode,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["PatternNode"]],
        parent: Optional["PatternNode"],
        root_node: Optional["PatternNode"],
    ) -> None:
        """
        Initialize a Command object.

        :param pattern_node_dict: A dictionary representing the pattern_node structure.
        :param name: The name of the pattern_node.
        :param times: Repeating information for the pattern_node execution.
        :param children: Sub-pattern_nods or child pattern_nods.
        :param pattern_nod_type: The type of the pattern_node (mnemonic, operand, etc.).
        :param parent: The parent pattern_node, if any.
        :param root_node: The root pattern_node of the pattern_node tree. This collects the capture group references.
        """
        self.pattern_node_dict = pattern_node_dict
        self.name = name
        self.times = times
        self.children = children
        self.parent = parent
        self.root_node = root_node

    @abstractmethod
    def get_regex(self) -> str:
        """Get regex from a leaf or call a recursion over the branch."""


class PatternNodeBase(PatternNode):
    """
    Base class for the pattern node with dummy implementation of the get_regex method.
    This is a temporary solution until the node type is defined and we can implement the actual concrete class
    """

    def get_regex(self) -> str:
        raise NotImplementedError("This is a base class and should not be used directly.")
