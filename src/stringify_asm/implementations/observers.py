"Observers implementation module"

from typing import Optional
from src.stringify_asm.abstracts.abs_observer import InstructionObserver, Instruction


class TagOutofAddrsRangeJumps(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, max_addr: str) -> None:
        self.max_addr = max_addr

    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        if inst.addrs > self.max_addr:
            return self.deal_with_instruction_out_of_range(inst)
        return inst

    def deal_with_instruction_out_of_range(self, inst: Instruction) -> Instruction:
        # TODO: implement
        return inst


class CheckAddrRangeJumpsNearBadInstruction(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, livehood: int) -> None:
        # Set number of instructions the bad instruction may affect until alignment
        self.livehood = livehood
        self.current_instructions_index = 0

    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        # Check instructions

        # Instructions in the range of a bad instruction
        if self.current_instructions_index <= self.livehood:
            self.current_instructions_index = 0
            return self.tag_instruction(inst)

        # Instruction out of the range of a bad instruction
        self.current_instructions_index += 1
        return inst

    def tag_instruction(self, inst: Instruction) -> Instruction:
        # TODO: implement
        return inst


class RemoveEmptyInstructions(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        # Check instructions
        if not inst.mnemonic == "empty":
            return inst
        return None
