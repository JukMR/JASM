from typing import Final, List

import regex

from jasm.global_definitions import (
    Instruction,
    MatchingSearchMode,
)
from jasm.logging_config import logger
from src.jasm.match.abstracts.i_matched_observer import IMatchedObserver
from src.jasm.match.implementations.instruction_observer_consumer import InstructionObserverConsumer


class CompleteConsumer(InstructionObserverConsumer):
    def __init__(
        self,
        regex_rule: str,
        matched_observer: IMatchedObserver,
        matching_mode: MatchingSearchMode,
        return_only_address: bool,
    ) -> None:
        super().__init__(regex_rule=regex_rule, matched_observer=matched_observer)
        self._all_instructions: str = ""
        self._all_instructions_list: List[str] = []
        self.matching_mode = matching_mode
        self.timeout_regex: Final = 60
        self.return_only_addresses: bool = return_only_address

    def consume_instruction(self, inst: Instruction) -> None:
        processed_inst = self._process_instruction(inst)
        if processed_inst:
            self._all_instructions_list.append(processed_inst.stringify() + ",|")

    @staticmethod
    def get_first_addr_from_regex_result(regex_result: str) -> str:
        return regex_result.split("::")[0]

    def finalize(self) -> None:

        self._all_instructions = "".join(self._all_instructions_list)
        logger.debug("Finalized with instructions: \n%s", self._all_instructions)

        # TODO: find the right way to do this
        # Add stringified instructions to the observer to test them in test_parsing
        self._matched_observer.stringified_instructions = self._all_instructions

        match self.matching_mode:
            case MatchingSearchMode.first_find:  # return first finding
                logger.info("Matching first occurence")
                self.do_match_first_occurence()

            case MatchingSearchMode.all_finds:  # return all findings
                logger.info("Matching all findings")
                self.do_match_all_findings()

        super().finalize()

    def do_match_first_occurence(self) -> None:
        """Match the first occurence of the regex in the instructions"""
        try:
            match_result = regex.search(
                pattern=self._regex_rule, string=self._all_instructions, timeout=self.timeout_regex
            )

        except TimeoutError as exc:
            logger.error("Regex timeout")
            raise ValueError("Regex timeout") from exc

        if match_result:

            if self.return_only_addresses:
                # Returning just the address
                addr = self.get_first_addr_from_regex_result(match_result.group(0))
                self._matched_observer.regex_matched(addr)
            else:
                # Return address and main instruction
                self._matched_observer.regex_matched(match_result.group(0))

    def do_match_all_findings(self) -> None:
        """Match all findings of the regex in the instructions"""
        try:
            match_iterator = regex.finditer(
                pattern=self._regex_rule, string=self._all_instructions, timeout=self.timeout_regex
            )

        except TimeoutError as exc:
            logger.error("Regex timeout")
            raise ValueError("Regex timeout") from exc

        if match_iterator:
            for match_result in match_iterator:
                if match_result:
                    if self.return_only_addresses:
                        # Returning just the address
                        addr = self.get_first_addr_from_regex_result(match_result.group(0))
                        self._matched_observer.regex_matched(addr)
                    else:
                        # Return addresses and instructions
                        self._matched_observer.regex_matched(match_result.group(0))
