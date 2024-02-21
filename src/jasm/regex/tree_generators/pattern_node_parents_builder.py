from typing import List

from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeParentsBuilder:
    def __init__(self, command: PatternNode) -> None:
        self.command = command

    def set_parent(self, parent: PatternNode, children: List[PatternNode]) -> None:
        for child in children:
            child.parent = parent
            if child.children:  # Recursively set parent for the child's children
                assert isinstance(child.children, (List, str))
                self.set_parent(child, child.children)

    def build(self) -> None:
        if self.command.children:
            assert isinstance(self.command.children, List)
            self.set_parent(self.command, self.command.children)
