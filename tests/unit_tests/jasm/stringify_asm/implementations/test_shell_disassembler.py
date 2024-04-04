import pytest
from unittest.mock import patch, MagicMock
from jasm.stringify_asm.implementations.shell_disassembler import ShellDisassembler


@pytest.fixture
def shell_disassembler() -> ShellDisassembler:
    program = "fake_disassembler"
    flags = ["--flag1", "--flag2"]
    return ShellDisassembler(program, flags)


# Successful Disassembly
@patch("jasm.stringify_asm.implementations.shell_disassembler.Path.exists", return_value=True)
@patch("subprocess.run")
def test_disassemble_success(
    mock_run: MagicMock, mock_exists: MagicMock, shell_disassembler: ShellDisassembler
) -> None:
    mock_run.return_value = MagicMock(returncode=0, stdout="disassembled content")
    input_file = "path/to/binary"
    result = shell_disassembler.disassemble(input_file)
    assert result == "disassembled content"
    mock_run.assert_called_once_with(
        ["fake_disassembler", "--flag1", "--flag2", input_file],
        capture_output=True,
        text=True,
        check=True,
    )


@patch("jasm.stringify_asm.implementations.shell_disassembler.Path.exists", return_value=True)
@patch("subprocess.run")
@patch("jasm.logging_config.logger.info")
def test_disassemble_success_log(
    mock_info: MagicMock, mock_run: MagicMock, mock_exists: MagicMock, shell_disassembler: ShellDisassembler
) -> None:
    mock_run.return_value = MagicMock(returncode=0, stdout="disassembled content")
    input_file = "path/to/binary"
    result = shell_disassembler.disassemble(input_file)
    assert result == "disassembled content"
    mock_info.assert_called_once_with("File binary successfully disassembled")


# File not found
@patch("jasm.stringify_asm.implementations.shell_disassembler.Path.exists", return_value=False)
def test_disassemble_file_not_found(mock_exists: MagicMock, shell_disassembler: ShellDisassembler) -> None:
    input_file = "nonexistent/path"
    with pytest.raises(AssertionError):
        shell_disassembler.disassemble(input_file)


# Disassembly Program Not Found
@patch("jasm.stringify_asm.implementations.shell_disassembler.Path.exists", return_value=True)
@patch("subprocess.run", side_effect=FileNotFoundError)
@patch("jasm.logging_config.logger.error")
def test_disassemble_program_not_found(
    mock_error: MagicMock, mock_run: MagicMock, mock_exists: MagicMock, shell_disassembler: ShellDisassembler
) -> None:
    input_file = "path/to/binary"
    with pytest.raises(FileNotFoundError):
        shell_disassembler.disassemble(input_file)
    mock_error.assert_called()


# General Error Handling
@patch("jasm.stringify_asm.implementations.shell_disassembler.Path.exists", return_value=True)
@patch("subprocess.run", side_effect=Exception("General error"))
@patch("jasm.logging_config.logger.error")
def test_disassemble_general_error(
    mock_error: MagicMock, mock_run: MagicMock, mock_exists: MagicMock, shell_disassembler: ShellDisassembler
) -> None:
    input_file = "path/to/binary"
    with pytest.raises(Exception) as exc_info:
        shell_disassembler.disassemble(input_file)
    assert "General error" in str(exc_info.value)
    mock_error.assert_called_with("Error while disassembling file: %s", exc_info.value)
