from jasm.regex.tree_generators.shared_context import SharedContext


class CaptureGroupInterface:
    @staticmethod
    def has_any_ancestor_who_is_capture_group_reference(shared_context: SharedContext, pattern_node_name: str) -> bool:
        "Check if any ancestor is a capture group reference"

        assert isinstance(shared_context, SharedContext)
        assert isinstance(pattern_node_name, str)

        if not shared_context.is_initialized():
            return False

        return shared_context.capture_is_registered(pattern_node_name)

    @staticmethod
    def add_new_references_to_global_list(shared_context: SharedContext, pattern_node_name: str) -> None:
        "Add new references to global list"

        assert isinstance(shared_context, SharedContext)
        assert isinstance(pattern_node_name, str)

        if not shared_context.is_initialized():
            shared_context.initialize()

        if not shared_context.capture_is_registered(pattern_node_name):
            shared_context.add_capture(pattern_node_name)
