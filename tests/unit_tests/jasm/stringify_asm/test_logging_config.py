import os
from tempfile import TemporaryDirectory
from typing import List
from unittest.mock import MagicMock, mock_open, patch

from jasm.logging_config import LazyFileHandler, _get_date_string_for_filename, configure_logger, logger


@patch("jasm.logging_config.Path.mkdir")
def test_log_file_naming(mock_mkdir):
    date = "2023_01_01_12_00_00"
    filename = _get_date_string_for_filename(log_type="DEBUG", date=date)
    expected_filename = "logs/DEBUG/2023_01_01_12_00_00.log"
    assert filename == expected_filename
    mock_mkdir.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
def test_lazy_file_handler(mock_open):
    handler = LazyFileHandler("test.log")
    mock_record = MagicMock()
    handler.emit(mock_record)
    mock_open.assert_called_once_with("test.log", "a", encoding=None)


def test_logger_configuration():
    with TemporaryDirectory() as temp_dir:

        # Redirect log output to the temporary directory
        os.chdir(temp_dir)
        configure_logger(debug=True, info=False, enable_log_to_file=True, enable_log_to_terminal=False)

        logger.debug("Test debug message")

        # Check if the log file with the debug message exists
        log_files = list_files_in_subdirs(temp_dir)

        assert len(log_files) > 0
        # Additional assertions can be made regarding the contents of the log file


def list_files_in_subdirs(temp_dir: str) -> List[str]:
    """
    List all files in the subdirectories of temp_dir.

    Args:
    - temp_dir (str): The directory to search within.

    Returns:
    - List[str]: A list of paths to files within subdirectories of temp_dir.
    """
    log_files = []
    for dirpath, _, filenames in os.walk(temp_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.isfile(file_path):
                log_files.append(file_path)
    return log_files
