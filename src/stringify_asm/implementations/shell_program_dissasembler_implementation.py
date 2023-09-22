import subprocess
from src.stringify_asm.abstracts.disassemble_abstract import Disassembler


class ShellProgramDissasembler(Disassembler):
    """A class to disassemble binaries using a shell program."""

    def __init__(self, binary: str, output_path: str, program: str, flags: str) -> None:
        super().__init__(binary=binary, output_path=output_path)
        self.program = program
        self.flags = flags

    def _write_to_disk(self, data: str) -> None:
        """Write the provided data to the output path."""
        with open(self.output_path, "w", encoding="utf-8") as fd:
            fd.write(data)

    def _run_program(self) -> None:
        """Run the shell program to disassemble the binary."""
        try:
            result = subprocess.run(
                [self.program, self.flags, self.binary],
                capture_output=True,
                text=True,
                check=True,
            )

            # Check the command executed correctly
            if result.returncode == 0:
                self._write_to_disk(result.stdout)
                print(f"File binary successfully disassembled to {self.output_path}")
            else:
                raise ValueError(f"Error while disassembling file. Return code error: {result.stderr}")

        except FileNotFoundError as exc:
            raise ValueError(
                f"Error: program '{self.program}' not found. Ensure it's installed and in your system PATH."
            ) from exc

    def disassemble(self) -> None:
        """Disassemble the binary using the provided flags and program."""
        self._run_program()
