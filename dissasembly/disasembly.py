import subprocess


class Disassembler:
    def write_to_disk(self, data: str):
        with open('dissasembled.s', 'w', encoding='utf-8') as file:
            file.write(data)

    def _binary_disambler(self, program: str,
                          flags: str,
                          binary: str
                          ) -> str | None:
        try:
            result = subprocess.run(
                [program, flags, binary], capture_output=True, text=True)

        # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                self.write_to_disk(result.stdout)
            else:
                # Return the error message, if any
                return f"Error: {result.stderr}"

        except FileNotFoundError:
            return f"Error: program not found. Make sure you have {program} installed and in your system PATH."

    def dissamble_with_objdump(self, binary: str):
        return self._binary_disambler(program='objdump', flags='d', binary=binary)

    def dissamble_with_llvm(self, binary: str):
        return self._binary_disambler(program='llvm-objdump', flags='d', binary=binary)


if __name__ == "__main__":
    Disassembler().dissamble_with_objdump(binary='/bin/ls')
