from pathlib import Path
import subprocess

from jasm.logging_config import logger
from jasm.stringify_asm.abstracts.disassembler import Disassembler

# from typing import override


class ShellDisassembler(Disassembler):
    """A class to disassemble binaries using a shell program."""

    def __init__(self, program: str, flags: list[str]) -> None:
        self.program = program
        self.flags = flags

    def disassemble(self, input_file: str) -> str:
        """Run the shell program to disassemble the binary."""
        try:
            assert Path(input_file).exists(), f"File '{input_file}' does not exist"
            result = subprocess.run(
                [self.program] + self.flags + [input_file],
                capture_output=True,
                text=True,
                check=True,
            )

            # Check the command executed correctly
            if result.returncode == 0:
                logger.info("File binary successfully disassembled")
                return result.stdout
            raise ValueError(f"Error while disassembling file. Return code error: {result.stderr}")

        except FileNotFoundError as exc:
            raise ValueError(
                f"Error: program '{self.program}' not found. Ensure it's installed and in your system PATH."
            ) from exc

        except Exception as exc:
            raise ValueError("Error while disassembling file.") from exc
