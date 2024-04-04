from jasm.regex.tree_generators.capture_manager import CapturesManager


class CaptureGroupHelper:
    @staticmethod
    def has_any_ancestor_who_is_capture_group_reference(
        capture_manager: CapturesManager, pattern_node_name: str
    ) -> bool:
        "Check if any ancestor is a capture group reference"

        assert isinstance(capture_manager, CapturesManager)
        assert isinstance(pattern_node_name, str)

        return capture_manager.capture_is_registered(pattern_node_name)  # type:ignore

    @staticmethod
    def add_new_references_to_global_list(capture_manager: CapturesManager, pattern_node_name: str) -> None:
        "Add new references to global list"

        assert isinstance(capture_manager, CapturesManager)
        assert isinstance(pattern_node_name, str)

        if not capture_manager.capture_is_registered(pattern_node_name):
            capture_manager.add_capture(pattern_node_name)
