# Parsed instruction tester module
#
# Module added in order to inspect the parsed instructions


from typing import Optional


# Enable parsing test or not
TESTER: bool = True


class Tester:
    def __init__(self) -> None:
        self.instructions: Optional[str] = None

    def send(self, stringified_instructions: str) -> None:
        self.instructions = stringified_instructions

    def read(self) -> str:
        if not self.instructions:
            raise ValueError("No instructions to read")
        return self.instructions
