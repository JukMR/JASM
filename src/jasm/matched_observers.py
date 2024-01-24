from src.jasm.logging_config import logger
from src.jasm.stringify_asm.abstracts.abs_observer import IMatchedObserver


class MatchedObserver(IMatchedObserver):
    """Observer that logs the matched address"""

    def __init__(self) -> None:
        self._matched = False
        self._stringified_instructions: str = ""

    @property
    def matched(self) -> bool:
        "Matched property for observer"
        return self._matched

    @property
    def stringified_instructions(self) -> str:
        return self._stringified_instructions

    @stringified_instructions.setter
    def stringified_instructions(self, value: str) -> None:
        self._stringified_instructions = value

    # @override
    def regex_matched(self, addr: str) -> None:
        self._matched = True
        logger.info("Matched address: %s", addr)

    # @override
    def finalize(self) -> None:
        if not self._matched:
            logger.info("RESULT: Pattern not found\n")
