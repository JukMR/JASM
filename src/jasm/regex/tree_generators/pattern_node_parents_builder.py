from typing import List

from jasm.regex.tree_generators.pattern_node import PatternNode


class PatternNodeParentsBuilder:
    def __init__(self, command: PatternNode) -> None:
        self.command = command

    def _set_parent(self, current_node: PatternNode) -> None:
        assert isinstance(current_node.children, List)
        children_nodes = current_node.children

        if current_node.parent is None:
            # This is the root node
            root_node = current_node
        else:
            # Spread the root_node down the tree
            root_node = current_node.root_node

        for child in children_nodes:
            child.parent = current_node
            child.root_node = root_node
            if child.children:  # Recursively set parent for the child's children
                self._set_parent(child)

    def build(self) -> None:
        if self.command.children:
            self._set_parent(self.command)
