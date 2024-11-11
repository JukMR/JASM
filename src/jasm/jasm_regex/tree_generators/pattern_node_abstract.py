"PatternNode definition file"

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from jasm.global_definitions import TimesType
from jasm.jasm_regex.tree_generators.shared_context import SharedContext


@dataclass
class PatternNodeData:
    name: str | int
    times: TimesType
    children: Optional[List["PatternNode"]]
    parent: Optional["PatternNode"]
    shared_context: SharedContext


class PatternNode(ABC):
    def __init__(self, pattern_node_data: PatternNodeData) -> None:
        """
        Initialize a Command object.

        :param name: The name of the pattern_node.
        :param times: Repeating information for the pattern_node execution.
        :param children: Sub-pattern_nods or child pattern_nods.
        :param parent: The parent pattern_node, if any.
        :param shared_context: Shared context for the pattern_node. This is used for storing capture group references.
        """
        self.name = pattern_node_data.name
        self.times = pattern_node_data.times
        self.children = pattern_node_data.children
        self.parent = pattern_node_data.parent
        self.shared_context = pattern_node_data.shared_context

    @abstractmethod
    def get_regex(self) -> str:
        """Get regex from a leaf or call a recursion over the branch."""
