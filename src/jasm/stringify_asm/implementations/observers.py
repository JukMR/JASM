"Observers implementation module"

from typing import Optional

from jasm.stringify_asm.abstracts.abs_observer import IConsumer, IInstructionObserver, Instruction


class TagOutofAddrsRangeJumps(IConsumer):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, max_addr: str) -> None:
        self.max_addr = max_addr

    def consume_instruction(self, inst: Instruction) -> None:
        if inst.addrs > self.max_addr:
            return self.deal_with_instruction_out_of_range(inst)
        return inst

    def deal_with_instruction_out_of_range(self, inst: Instruction) -> Instruction:
        # TODO: implement
        return inst


class CheckAddrRangeJumpsNearBadInstruction(IConsumer):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self, distance: int) -> None:
        # Set number of instructions the bad instruction may affect until alignment
        self.livehood = distance
        self.current_instructions_index = 0

    def consume_instruction(self, inst: Instruction) -> None:
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


class RemoveEmptyInstructions(IInstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    # @override
    def observe_instruction(self, inst: Instruction) -> Optional[Instruction]:
        # Check instructions
        if not inst.mnemonic == "empty":
            return inst
        return None