# logging_config.py

import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a custom logger
logger = logging.getLogger("main_app")
logger.setLevel(logging.DEBUG)

# handler = logging.FileHandler("main_app.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# logger.addHandler(handler)


def enable_debugging() -> None:
    logger.setLevel(logging.DEBUG)

def enable_info_level() -> None:
    logger.setLevel(logging.INFO)
