from jasm.regex.tree_generators.pattern_node_abstract import PatternNode


class PatternNodeTmpUntyped(PatternNode):  # type: ignore
    """
    Dummy class for the pattern node with dummy implementation of the get_regex method.
    This is a temporary solution until the node type is defined and we can implement the actual concrete class
    """

    def get_regex(self) -> str:
        raise NotImplementedError("This is a base class and should not be used directly.")
