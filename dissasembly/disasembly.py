import subprocess

class disassembler:
    def write_to_disk(self, data: str):
        with open('dissasembled.s', 'w', encoding='utf-8') as file:
            file.write(data)

    def objdump(self, binary: str) -> str | None:
        try:
            result = subprocess.run(['objdump', '-d', binary], capture_output=True, text=True)

        # Check the return code to see if the command executed successfully
            if result.returncode == 0:
                self.write_to_disk(result.stdout)
            else:
                return f"Error: {result.stderr}"  # Return the error message, if any


        except FileNotFoundError:
            return "Error: objdump command not found. Make sure you have 'objdump' installed and in your system PATH."

if __name__ == "__main__":
    disassembler().objdump(binary='/bin/ls')