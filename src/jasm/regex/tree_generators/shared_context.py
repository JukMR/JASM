from dataclasses import dataclass


@dataclass
class SharedContext:
    capture_group_references: list[str]

    def add_capture(self, entry: str) -> None:
        self.capture_group_references.append(entry)

    def get_capture_index(self, capture: str) -> int:
        for i, entry in enumerate(self.capture_group_references):
            if entry == capture:
                return i + 1

        raise ValueError(f"Capture group {capture} not found in {self.capture_group_references}")
