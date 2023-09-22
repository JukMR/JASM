from logging import DEBUG, ERROR, INFO, WARNING, Formatter, StreamHandler, Filter, getLevelName, getLogger
from datetime import datetime
from pathlib import Path


def _create_log_folder_if_not_exists(folder_name: str) -> Path:
    folder = Path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _get_date_string_for_filename(log_type: str) -> str:
    date = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    folder_name = f"logs/{log_type}"
    _create_log_folder_if_not_exists(folder_name)
    return f"{folder_name}/{date}.log"


class LogLevelFilter(Filter):
    def __init__(self, level) -> None:
        self.level = level

    def filter(self, record) -> bool:
        return record.levelno == self.level


logger = getLogger(__name__)


class LazyFileHandler(StreamHandler):
    """
    Custom logging handler that lazily opens the log file.
    The file is only opened when a log record is emitted, preventing the creation of empty log files.
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False):
        self.base_filename = filename
        self.mode = mode
        self.encoding = encoding
        self._file = None
        StreamHandler.__init__(self)

    def _open_file(self):
        if self._file is None:
            self._file = open(self.base_filename, self.mode, encoding=self.encoding)
        return self._file

    def emit(self, record):
        self.stream = self._open_file()
        StreamHandler.emit(self, record)


def _set_log_to_file(log_level):
    log_type = getLevelName(log_level)
    logfile = _get_date_string_for_filename(log_type)
    file_handler = LazyFileHandler(logfile)
    file_handler.setLevel(log_level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    level_filter = LogLevelFilter(log_level)
    file_handler.addFilter(level_filter)
    logger.addHandler(file_handler)


def _set_log_to_terminal(log_level):
    stream_handler = StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def configure_logger(debug: bool, info: bool, enable_log_to_file=True, enable_log_to_terminal=True) -> None:
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
