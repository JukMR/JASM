from typing import List
from jasm.logging_config import logger
from jasm.stringify_asm.abstracts.abs_observer import IMatchedObserver


class MatchedObserver(IMatchedObserver):
    """Observer that logs the matched address"""

    def __init__(self) -> None:
        self._matched: bool = False
        self._stringified_instructions: str = ""
        self.addr_list: List[str] = []

    @property
    def matched(self) -> bool:
        "Matched property for observer"
        return self._matched

    @matched.setter
    def matched(self, value: bool) -> None:
        "Matched property for observer"
        self._matched = value

    @property
    def stringified_instructions(self) -> str:
        return self._stringified_instructions

    @stringified_instructions.setter
    def stringified_instructions(self, value: str) -> None:
        self._stringified_instructions = value

    def regex_matched(self, addr: str) -> None:
        self.matched = True
        self.addr_list.append(addr)
        logger.info("Matched address: %s", addr)

    def finalize(self) -> None:
        if not self.matched:
            logger.info("RESULT: Pattern not found\n")
        else:
            logger.info("RESULT: Pattern found\n")
