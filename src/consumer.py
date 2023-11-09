from typing import List, Optional, Sequence

from src.logging_config import logger
from src.stringify_asm.abstracts.abs_observer import Instruction, InstructionObserver


class InstructionsAppender:
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, inst_list: Sequence[Optional[Instruction]]) -> None:
        self.inst_list = inst_list

    def stringify_inst_list(self) -> List[str]:
        return [inst.stringify() for inst in self.inst_list if inst]

    @staticmethod
    def join_inst_list_into_string(list_inst: List[str]) -> str:
        return ",|".join(list_inst) + ",|"

    def finalize(self) -> str:
        return self.join_inst_list_into_string(self.stringify_inst_list())


class Consumer:
    def __init__(self, inst_list: Sequence[Instruction]) -> None:
        self.inst_list = inst_list
        self.instruction_observers: List[InstructionObserver]

    def set_observers(self, instruction_observers: List[InstructionObserver]) -> None:
        self.instruction_observers = instruction_observers

    def execute_observers(self) -> Sequence[Optional[Instruction]]:
        observed_instructions: Sequence[Optional[Instruction]] = self.inst_list

        for observer in self.instruction_observers:
            observed_instructions = [
                observer.observe_instruction(inst)
                for inst in observed_instructions
                if observer.observe_instruction(inst)
            ]

        return observed_instructions

    def finalize(self) -> str:
        instruction_list_concatenated_strings = InstructionsAppender(self.inst_list).finalize()
        logger.debug("The concatenated stringified instruction list is: \n%s", instruction_list_concatenated_strings)

        return instruction_list_concatenated_strings
