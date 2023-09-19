"Dissasembler Implementation module"

import subprocess
from src.global_definitions import PathStr

from src.stringify_asm.abstracts.disassemble_abstract import Dissasembler, DissasembleMethod


class ShellProgramDissasembler(DissasembleMethod):
    """Shell Program Dissasembler Implementation"""

    def __init__(self, binary: str, output_path: str, program: str, flags: str) -> None:
        super().__init__(binary=binary, output_path=output_path)
        self.program = program
        self.flags = flags

    def _write_to_disk(self, data: str) -> None:
        if self.output_path is None:
            raise NotImplementedError("No path provided. Execute set_output_path() first")

        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(data)

    def _run_program(self) -> None:
        """Shell Program Dissasembler Implementation"""
        if self.binary is None:
            raise NotImplementedError("binary is not set yet. Should call set_binary() first")
        try:
            result = subprocess.run(
                [self.program, self.flags, self.binary],
                capture_output=True,
                text=True,
                check=True,
            )

            # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                self._write_to_disk(result.stdout)
                print(f"File binary successfully dissasembled to {self.output_path}")
            else:
                # Return the error message, if any
                raise ValueError(f"Error while dissasembling file. Error: {result.stderr}")

        except FileNotFoundError as exc:
            raise ValueError(
                f"Error: program: {self.program} not found. Make sure you to have it installed and in your system PATH."
            ) from exc

    def dissasemble(self) -> None:
        if self.flags is None:
            raise ValueError("flags not set yet. Should call set_flags() first")

        self._run_program()


class DissasembleImplementation(Dissasembler):
    "Dissasembler Implementation"

    def __init__(self, binary: PathStr, output_path: str, dissasemble_method: DissasembleMethod) -> None:
        super().__init__(binary=binary, output_path=output_path)
        self.dissasemble_method = dissasemble_method

    def get_assembly(self) -> None:
        "Dissasemble with objdump by_default"

        if self.dissasemble_method is None:
            raise NotImplementedError("dissasemble_program not set yet. Should call set_dissasemble_program() first.")

        # return self.dissasemble_program.dissasemble(program=self.dissasemble_program, flags="-d")
        return self.dissasemble_method.dissasemble()
