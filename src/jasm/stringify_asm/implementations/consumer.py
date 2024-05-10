from typing import Final, List, Optional

import regex

from jasm.global_definitions import MatchingSearchMode, Instruction
from jasm.logging_config import logger
from jasm.stringify_asm.abstracts.abs_observer import IConsumer, IInstructionObserver, IMatchedObserver


class InstructionObserverConsumer(IConsumer):  # type: ignore
    def __init__(self, regex_rule: str, matched_observer: IMatchedObserver) -> None:
        super().__init__(matched_observer=matched_observer)
        self.instruction_observers: List[IInstructionObserver] = []
        self.inst_list: List[Instruction]
        self._regex_rule: Final = regex_rule

    def add_observer(self, instruction_observer: IInstructionObserver) -> None:
        self.instruction_observers.append(instruction_observer)

    def _process_instruction(self, inst: Instruction) -> Optional[Instruction]:
        observed_instruction: Optional[Instruction] = inst
        for observer in self.instruction_observers:
            observed_instruction = observer.observe_instruction(inst)
            if not observed_instruction:
                break
        return observed_instruction

    def finalize(self) -> None:
        self._matched_observer.finalize()


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


# TODO: Implement this Consumer
# class StreamConsumer(InstructionObserverConsumer):

#     def consume_instruction_normal(self, inst: Instruction) -> None:
#         processed_inst = self._process_instruction(inst)
#         if processed_inst:
#             # Evaluate the instruction in the streaming regex engine
#             # TODO: implement this
#             # regex_engine.process(processed_inst)
#             # if regex_engine.matched:
#             #     self._matched_observer.regex_matched(processed_inst.addrs)
#             pass
