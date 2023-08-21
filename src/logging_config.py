"logging_config.py"

import logging
from datetime import datetime
from pathlib import Path


def _create_log_folder_if_not_exists() -> Path:
    "Create log folder"
    folder = Path("logs")
    folder.mkdir(parents=True, exist_ok=True)

    return folder


def _get_date_string_for_filename() -> str:
    date = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    logs_folder = _create_log_folder_if_not_exists()

    return f"{logs_folder.name}/{date}.log"


# Create a logger object
logger = logging.getLogger(__name__)


def set_log_to_file(log_level=logging.INFO) -> None:
    "Configure and enable logging to logfile"

    logfile = _get_date_string_for_filename()
    # Create a file handler to log messages to a file
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(log_level)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Set the formatter for the handler
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)


def set_log_to_terminal(log_level=logging.INFO):
    "Configure and enable logging to terminal"
    # Create a stream handler to log messages to the terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Set the formatter for the handler
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)


def configure_logger(debug: bool, info: bool, disable_log_to_file: bool, disable_log_to_terminal: bool) -> None:
    "Configure logger based on given log level"

    if debug:
        logger.setLevel(logging.DEBUG)

    elif info:
        logger.setLevel(logging.INFO)

    log_level = debug or info
    if not disable_log_to_file:
        set_log_to_file(log_level=log_level)

    if not disable_log_to_terminal:
        set_log_to_terminal(log_level=log_level)
