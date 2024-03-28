from dataclasses import dataclass

from jasm.regex.tree_generators.capture_manager import CapturesManager


@dataclass
class SharedContext:
    capture_manager: CapturesManager
