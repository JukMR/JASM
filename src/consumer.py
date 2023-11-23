import re
from typing import Final, List, Optional

from src.logging_config import logger
from src.stringify_asm.abstracts.abs_observer import IConsumer, IInstructionObserver, IMatchedObserver, Instruction


class InstructionObserverConsumer(IConsumer):
    def __init__(self, regex_rule: str, matched_observer: IMatchedObserver) -> None:
        super().__init__(matched_observer=matched_observer)
        self.instruction_observers: List[IInstructionObserver] = []
        self.inst_list: List[Instruction]
        self._regex_rule: Final = regex_rule

    def add_observer(self, instruction_observer: IInstructionObserver) -> None:
        self.instruction_observers.append(instruction_observer)

    # @override
    def _process_instruction(self, inst: Instruction) -> Optional[Instruction]:
        observed_instruction: Optional[Instruction] = inst
        for observer in self.instruction_observers:
            observed_instruction = observer.observe_instruction(inst)
            if not observed_instruction:
                break
        return observed_instruction

    # @override
    def finalize(self) -> None:
        return self._matched_observer.finalize()


class CompleteConsumer(InstructionObserverConsumer):
    def __init__(self, regex_rule: str, matched_observer: IMatchedObserver) -> None:
        super().__init__(
            regex_rule=regex_rule,
            matched_observer=matched_observer,
        )
        self._all_instructions: str = ""

    # @override
    def consume_instruction(self, inst: Instruction) -> None:
        processed_inst = self._process_instruction(inst)
        if processed_inst:
            self._all_instructions += processed_inst.stringify() + ",|"

    # @override
    def finalize(self) -> None:
        # TODO: find the right way to do this
        # Add stringified instructions to the observer to test them in test_parsing

        self._matched_observer.stringified_instructions = self._all_instructions

        match_result = re.search(pattern=self._regex_rule, string=self._all_instructions)

        if match_result:

            def get_first_addr_from_regex_result(regex_result: str) -> str:
                regex_result = regex_result.split("::")[0]
                return regex_result

            addr = get_first_addr_from_regex_result(match_result.group(0))
            self._matched_observer.regex_matched(addr)
        logger.debug("Finalized with instructions: %s", self._all_instructions)

        super().finalize()


class StreamConsumer(InstructionObserverConsumer):
    # @override
    def consume_instruction(self, inst: Instruction) -> None:
        processed_inst = self._process_instruction(inst)
        if processed_inst:
            # Evaluate the instruction in the streaming regex engine
            # TODO: implement this
            # regex_engine.process(processed_inst)
            # if regex_engine.matched:
            #     self._matched_observer.regex_matched(processed_inst.addrs)
            pass
