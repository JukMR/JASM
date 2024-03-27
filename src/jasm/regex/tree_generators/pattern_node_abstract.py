"PatternNode definition file"

from abc import ABC, abstractmethod
from typing import List, Optional

from jasm.global_definitions import TimeType


class PatternNode(ABC):
    def __init__(
        self,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["PatternNode"]],
        parent: Optional["PatternNode"],
        root_node: Optional["PatternNode"],
    ) -> None:
        """
        Initialize a Command object.

        :param name: The name of the pattern_node.
        :param times: Repeating information for the pattern_node execution.
        :param children: Sub-pattern_nods or child pattern_nods.
        :param parent: The parent pattern_node, if any.
        :param root_node: The root pattern_node of the pattern_node tree. This collects the capture group references.
        """
        self.name = name
        self.times = times
        self.children = children
        self.parent = parent
        self.root_node = root_node

    @abstractmethod
    def get_regex(self) -> str:
        """Get regex from a leaf or call a recursion over the branch."""
