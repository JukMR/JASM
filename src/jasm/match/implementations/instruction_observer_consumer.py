from typing import Final, List, Optional

from jasm.global_definitions import Instruction
from src.jasm.match.abstracts.i_consumer import IConsumer
from src.jasm.match.abstracts.i_matched_observer import IMatchedObserver
from src.jasm.stringify_asm.abstracts.i_instruction_observer import IInstructionObserver


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
