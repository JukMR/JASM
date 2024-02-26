import subprocess
from pathlib import Path
from subprocess import CalledProcessError

from jasm.global_definitions import BinaryFileFormatNotSupported
from jasm.logging_config import logger
from jasm.stringify_asm.abstracts.disassembler import Disassembler


class ShellDisassembler(Disassembler):
    """A class to disassemble binaries using a shell program."""

    def __init__(self, program: str, flags: list[str]) -> None:
        self.program = program
        self.flags = flags

    # @overrides
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
            logger.error("Error: program '%s' not found. Ensure it's installed and in your system PATH.", self.program)
            raise FileNotFoundError() from exc

        except CalledProcessError as exc:
            # Error when calling decompliler, probably due to binary file format not supported
            raise BinaryFileFormatNotSupported(exc.stderr) from exc

        except Exception as exc:
            logger.error("Error while disassembling file: %s", exc)
            raise exc
