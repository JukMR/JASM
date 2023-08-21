"Observers implementation module"

from src.stringify_asm.observer_abstract import InstructionObserver, Instruction


class InstructionsAppender(InstructionObserver):
    "InstructionObserver implementation that only concatenates instructions"

    def __init__(self) -> None:
        self.str_binary = ""

    def observe_instruction(self, inst: Instruction) -> None:
        self.str_binary += inst.stringify() + "," + "|"

    def finalize(self) -> str:
        return self.str_binary
