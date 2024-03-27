from dataclasses import dataclass
from typing import Optional


@dataclass
class SharedContext:
    capture_group_references: Optional[list[str]] = None

    def add_capture(self, entry: str) -> None:
        if self.capture_group_references is None:
            raise ValueError("Capture group references is None")

        self.capture_group_references.append(entry)

    def get_capture_index(self, capture: str) -> int:

        if self.capture_group_references is None:
            raise ValueError("Capture group references is None")

        for i, entry in enumerate(self.capture_group_references):
            if entry == capture:
                return i + 1

        raise ValueError(f"Capture group {capture} not found in {self.capture_group_references}")
