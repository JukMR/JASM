from datetime import datetime
from logging import DEBUG, ERROR, INFO, WARNING, Filter, Formatter, LogRecord, StreamHandler, getLevelName, getLogger
from pathlib import Path
from typing import Any, Optional


def _create_log_folder_if_not_exists(folder_name: str) -> Path:
    folder = Path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_current_date() -> str:
    return datetime.today().strftime("%Y_%m_%d_%H_%M_%S")


def _get_date_string_for_filename(log_type: str, date: str) -> str:
    folder_name = f"logs/{log_type}"
    _create_log_folder_if_not_exists(folder_name)
    return f"{folder_name}/{date}.log"


class LogLevelFilter(Filter):
    def __init__(self, level: int) -> None:
        super().__init__()
        self.level = level

    def filter(self, record: LogRecord) -> bool:
        return record.levelno == self.level


logger = getLogger(__name__)
logger.setLevel(WARNING)


class LazyFileHandler(StreamHandler):  # type: ignore
    """
    Custom logging handler that lazily opens the log file.
    The file is only opened when a log record is emitted, preventing the creation of empty log files.
    """

    def __init__(self, filename: str, mode: str = "a", encoding: Any = None) -> None:

        self.base_filename = filename
        self.mode = mode
        self.encoding = encoding
        self._file: Optional[Any] = None
        StreamHandler.__init__(self)

    def _open_file(self) -> Optional[Any]:
        if self._file is None:
            self._file = open(  # pylint: disable=consider-using-with
                self.base_filename, self.mode, encoding=self.encoding
            )
        return self._file

    def emit(self, record: LogRecord) -> None:
        self.stream = self._open_file()
        StreamHandler.emit(self, record)


def _set_log_to_file(log_level: int) -> None:
    log_type = getLevelName(log_level)
    date = get_current_date()
    logfile = _get_date_string_for_filename(log_type=log_type, date=date)
    file_handler = LazyFileHandler(logfile)
    file_handler.setLevel(log_level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    level_filter = LogLevelFilter(log_level)
    file_handler.addFilter(level_filter)
    logger.addHandler(file_handler)


def _set_log_to_terminal(log_level: int) -> None:
    stream_handler = StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def configure_logger(
    debug: bool, info: bool, enable_log_to_file: bool = True, enable_log_to_terminal: bool = True
) -> None:
    if debug:
        logger.setLevel(DEBUG)
    elif info:
        logger.setLevel(INFO)

    if enable_log_to_file:
        _set_log_to_file(ERROR)
        _set_log_to_file(WARNING)
        _set_log_to_file(INFO)
        _set_log_to_file(DEBUG)

    if enable_log_to_terminal:
        _set_log_to_terminal(DEBUG if debug else INFO)
