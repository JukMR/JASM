from typing import TypeAlias


Capture: TypeAlias = str


class CapturesManager:

    def __init__(self) -> None:
        self._capture_group_references: list[Capture] = []

    @property
    def capture_group_references(self) -> list[Capture]:
        return self._capture_group_references

    def add_capture(self, entry: Capture) -> None:
        self._capture_group_references.append(entry)

    def get_capture_index(self, capture: Capture) -> int:

        for i, entry in enumerate(self._capture_group_references):
            if entry == capture:
                return i + 1

        raise ValueError(f"Capture group {capture} not found in {self._capture_group_references}")

    def capture_is_registered(self, capture: Capture) -> bool:

        return capture in self._capture_group_references
