from jasm.regex.tree_generators.capture_group_index import CaptureGroupIndexOperandCall
from jasm.regex.tree_generators.deref_classes import DerefObject, DerefObjectBuilder
from jasm.regex.tree_generators.pattern_node_abstract import PatternNode
from jasm.regex.tree_generators.pattern_node_implementations.time_type_builder import TimesTypeBuilder


class PatternNodeDerefProperty(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        if self.children:
            assert isinstance(self.children, list)
            assert len(self.children) == 1

            child_regex: str = self.children[0].get_regex()
            return child_regex

        return str(self.name)


class PatternNodeDeref(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        times_regex = TimesTypeBuilder().get_min_max_regex(times=self.times)

        deref_object: DerefObject = DerefObjectBuilder(self).build()
        deref_regex = deref_object.get_regex()

        if times_regex:
            return f"(?:{deref_regex},){times_regex}"
        return f"{deref_regex},"


class PatternNodeDerefPropertyCaptureGroupReference(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return r"([^,|]+)"


class PatternNodeDerefPropertyCaptureGroupCall(PatternNode):  # type: ignore

    def get_regex(self) -> str:
        return CaptureGroupIndexOperandCall(pattern_node=self).to_regex()  # type: ignore
