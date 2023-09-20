"Dissasembler Implementation module"

from src.global_definitions import PathStr

from src.stringify_asm.abstracts.disassemble_abstract import Disassembler
from src.stringify_asm.abstracts.disassembler_method_abstract import DisassembleMethod


class DissasembleImplementation(Disassembler):
    "Dissasembler Implementation"

    def __init__(self, binary: PathStr, output_path: str, dissasemble_method: DisassembleMethod) -> None:
        super().__init__(binary=binary, output_path=output_path)
        self.dissasemble_method = dissasemble_method

    def get_assembly(self) -> None:
        "Dissasemble with objdump by_default"

        if self.dissasemble_method is None:
            raise NotImplementedError("dissasemble_program not set yet. Should call set_dissasemble_program() first.")

        # return self.dissasemble_program.dissasemble(program=self.dissasemble_program, flags="-d")
        return self.dissasemble_method.disassemble()
