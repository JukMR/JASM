"Dissasembler Implementation module"

import subprocess
from typing import Optional

from src.global_definitions import PathStr


class DissasembleImplementation:
    "Dissasembler Implementation"

    def __init__(self) -> None:
        self.binary: Optional[str] = None
        self.output_path: Optional[PathStr] = None
        self.dissasemble_program: Optional[str] = None

    def set_binary(self, binary: str) -> None:
        "Set binary for DissasembleImplementation class"

        self.binary = binary

    def set_output_path(self, output_path: PathStr) -> None:
        "Set output_path for DissasembleImplementation class"

        self.output_path = output_path

    def _write_to_disk(self, data: str) -> None:
        if self.output_path is None:
            raise NotImplementedError("No path provided. Execute set_output_path() first")

        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(data)

    def _binary_dissasemble(self, program: str, flags: str) -> None:
        if self.binary is None:
            raise NotImplementedError("binary is not set yet. Should call set_binary() first")
        try:
            result = subprocess.run(
                [program, flags, self.binary],
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
                f"Error: program: {program} not found. Make sure you to have it installed and in your system PATH."
            ) from exc

    def set_dissasemble_program(self, program: str) -> None:
        """
        Set dissasemble main program.
        Currently objdump and llvm supported and tested
        """

        self.dissasemble_program = program

    def dissasemble(self) -> None:
        "Dissasemble with objdump by_default"

        if self.dissasemble_program is None:
            raise NotImplementedError("dissasemble_program not set yet. Should call set_dissasemble_program() first.")

        return self._binary_dissasemble(program=self.dissasemble_program, flags="-d")
