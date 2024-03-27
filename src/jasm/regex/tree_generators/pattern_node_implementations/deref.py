from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperand
from jasm.regex.tree_generators.deref_classes import DerefObject, DerefObjectBuilder
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.capture_group.capture_group_call_common import (
    CaptureGroupCallRegexBuilder,
)
from jasm.regex.tree_generators.pattern_node_implementations.time_type_builder import TimeTypeBuilder


class PatternNodeDerefProperty(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.process_deref_child()

    def process_deref_child(self) -> str:
        if self.children:
            assert isinstance(self.children, list)
            assert len(self.children) == 1

            child_regex = self.children[0].get_regex()
            return child_regex

        return str(self.name)


class PatternNodeDeref(PatternNode):

    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.process_deref()

    def process_deref(self) -> str:
        times_regex = TimeTypeBuilder().get_min_max_regex(times=self.times)

        deref_object: DerefObject = DerefObjectBuilder(self).build()
        deref_regex = deref_object.get_regex()

        if times_regex:
            return f"(?:{deref_regex},){times_regex}"
        return f"{deref_regex},"


class PatternNodeDerefPropertyCaptureGroupReference(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_reference_deref()

    @staticmethod
    def get_capture_group_reference_deref() -> str:
        return r"([^,|]+)"


class PatternNodeDerefPropertyCaptureGroupCall(PatternNode):
    def __init__(self, pattern_node: PatternNode) -> None:
        super().__init__(
            name=pattern_node.name,
            times=pattern_node.times,
            children=pattern_node.children,
            parent=pattern_node.parent,
            shared_context=pattern_node.shared_context,
        )

    def get_regex(self) -> str:
        return self.get_capture_group_call_operand()

    def get_capture_group_call_operand(self) -> str:
        """Capture group call operand"""

        capture_group_instance = CaptureGroupIndexOperand(pattern_node=self)
        return CaptureGroupCallRegexBuilder(capture_group_instance).build()
