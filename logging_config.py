'logging_config.py'

import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a custom logger
logger = logging.getLogger("main_app")
logger.setLevel(logging.DEBUG)

def add_log_file(filename: str):
    'Add a log file'
    handler = logging.FileHandler(f"{filename}.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def enable_debugging() -> None:
    'Logger: Set DEBUG level'
    logger.setLevel(logging.DEBUG)

def enable_info_level() -> None:
    'Logger: Set INFO level'
    logger.setLevel(logging.INFO)
