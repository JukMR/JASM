class SharedContext:
    _capture_group_references: list[str]
    _initialized: bool = False

    def initialize(self) -> None:
        if self._initialized:
            raise ValueError("SharedContext already initialized")

        self._initialized = True
        self._capture_group_references = []

    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def capture_group_references(self) -> list[str]:
        if not self._initialized:
            raise ValueError("SharedContext not initialized")

        return self._capture_group_references

    def add_capture(self, entry: str) -> None:
        if not self._initialized:
            raise ValueError("SharedContext not initialized")

        self._capture_group_references.append(entry)

    def get_capture_index(self, capture: str) -> int:
        if not self._initialized:
            raise ValueError("SharedContext not initialized")

        for i, entry in enumerate(self._capture_group_references):
            if entry == capture:
                return i + 1

        raise ValueError(f"Capture group {capture} not found in {self._capture_group_references}")

    def capture_is_registered(self, capture: str) -> bool:
        if not self._initialized:
            raise ValueError("SharedContext not initialized")

        return capture in self._capture_group_references
