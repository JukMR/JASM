"PatternNode definition file"

from abc import ABC, abstractmethod
from typing import List, Optional

from jasm.global_definitions import TimeType
from jasm.regex.tree_generators.shared_context import SharedContext


class PatternNode(ABC):
    def __init__(
        self,
        name: str | int,
        times: TimeType,
        children: Optional[dict | List["PatternNode"]],
        parent: Optional["PatternNode"],
        shared_context: SharedContext,
    ) -> None:
        """
        Initialize a Command object.

        :param name: The name of the pattern_node.
        :param times: Repeating information for the pattern_node execution.
        :param children: Sub-pattern_nods or child pattern_nods.
        :param parent: The parent pattern_node, if any.
        :param shared_context: Shared context for the pattern_node. This is used for storing capture group references.
        """
        self.name = name
        self.times = times
        self.children = children
        self.parent = parent
        self.shared_context = shared_context

    @abstractmethod
    def get_regex(self) -> str:
        """Get regex from a leaf or call a recursion over the branch."""
