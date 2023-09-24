"Observers implementation module"

from typing import List
from src.stringify_asm.abstracts.abs_observer import InstructionObserver, Instruction


class InstructionsAppender(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self) -> None:
        self.instructions = []

    def observe_instruction(self, inst: Instruction) -> None:
        self.instructions.append(inst.stringify())

    def finalize(self) -> str:
        return ",|".join(self.instructions) + ",|"


class TagOutofAddrsRangeJumps(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, max_addr: str) -> None:
        self.instructions = []
        self.max_addr = max_addr

    def observe_instruction(self, inst: Instruction) -> None:
        current_addr = self.get_instruction_addr(inst)
        if current_addr > self.max_addr:
            self.instructions.append(self.deal_with_instruction_out_of_range(inst))
        self.instructions.append(inst.stringify())

    def finalize(self) -> List[str]:
        return self.instructions

    def get_instruction_addr(self, inst: Instruction) -> str:
        # TODO: implement
        return ""

    def deal_with_instruction_out_of_range(self, inst: Instruction) -> str:
        # TODO: implement
        return inst.stringify()


class CheckAddrRangeJumpsNearBadInstruction(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, livehood: int) -> None:
        self.instructions = []

        # Set number of instructions the bad instruction may affect until alignment
        self.livehood = livehood
        self.current_instructions_index = 0

    def observe_instruction(self, inst: Instruction) -> None:
        # Check instructions

        # Instructions in the range of a bad instruction
        if self.current_instructions_index <= self.livehood:
            self.instructions.append(self.tag_instruction(inst))
            self.current_instructions_index = 0

        # Instruction out of the range of a bad instruction
        else:
            self.instructions.append(inst.stringify())
            self.current_instructions_index += 1

    def tag_instruction(self, inst: Instruction) -> str:
        # TODO: implement
        return inst.stringify()

    def finalize(self) -> List[str]:
        return self.instructions
