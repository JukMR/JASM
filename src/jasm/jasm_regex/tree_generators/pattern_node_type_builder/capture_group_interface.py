from abc import ABC, abstractmethod
from jasm.jasm_regex.tree_generators.capture_manager import CapturesManager
from jasm.jasm_regex.tree_generators.pattern_node_abstract import PatternNode


class CaptureGroupBaseBuilder(ABC):

    def _capture_is_registered(
        self, capture_manager: CapturesManager, pattern_node_name: str
    ) -> bool:
        "check if it's a capture group already registered"
        return capture_manager.capture_is_registered(pattern_node_name)

    def add_new_references_to_global_list(
        self, capture_manager: CapturesManager, pattern_node_name: str
    ) -> None:
        "Add new references to global list"
        if not capture_manager.capture_is_registered(pattern_node_name):
            capture_manager.add_capture(pattern_node_name)

    def build(self, untyped_node: PatternNode) -> PatternNode:
        if self._capture_is_registered(
            untyped_node.shared_context.capture_manager, untyped_node.name
        ):
            # instance the class that will build the capture group
            return self._process_call(untyped_node)

        self.add_new_references_to_global_list(
            untyped_node.shared_context.capture_manager, untyped_node.name
        )
        return self._process_register(untyped_node)

    @abstractmethod
    def _process_call(self, untyped_node: PatternNode) -> PatternNode:
        pass

    @abstractmethod
    def _process_register(self, untyped_node: PatternNode) -> PatternNode:
        pass
