import subprocess
from src.stringify_asm.abstracts.disassembler_method_abstract import DisassembleMethod


class ShellProgramDissasembler(DisassembleMethod):
    """A class to disassemble binaries using a shell program."""

    def __init__(self, binary: str, output_path: str, program: str, flags: str) -> None:
        super().__init__(binary=binary, output_path=output_path)
        self.program = program
        self.flags = flags

    def _write_to_disk(self, data: str) -> None:
        """Write the provided data to the output path."""
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write(data)

    def _run_program(self) -> None:
        """Run the shell program to disassemble the binary."""
        if not self.binary:
            raise ValueError("Binary is not set yet. Should call set_binary() first.")

        try:
            result = subprocess.run(
                [self.program, self.flags, self.binary],
                capture_output=True,
                text=True,
                check=True,
            )

            if result.returncode == 0:
                self._write_to_disk(result.stdout)
                print(f"File binary successfully disassembled to {self.output_path}")
            else:
                raise ValueError(f"Error while disassembling file. Error: {result.stderr}")

        except FileNotFoundError as exc:
            raise ValueError(
                f"Error: program '{self.program}' not found. Ensure it's installed and in your system PATH."
            ) from exc

    def disassemble(self) -> None:
        """Disassemble the binary using the provided flags and program."""
        if not self.flags:
            raise ValueError("Flags not set yet. Should call set_flags() first.")

        self._run_program()
