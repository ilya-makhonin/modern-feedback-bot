import logging
import os


def log(name='main', file='logs.log', level='DEBUG'):
    logging_types = dict(
        DEBUG=logging.DEBUG,
        INFO=logging.INFO,
        WARNING=logging.WARNING,
        ERROR=logging.ERROR,
        CRITICAL=logging.CRITICAL)

    if not os.path.exists('logs/'):
        os.mkdir('./logs/')

    logger = logging.getLogger(name)
    logging_level = logging_types.get(level) if logging_types.get(level) else logging_types.get('DEBUG')
    logger.setLevel(logging_level)
    file_handler = logging.FileHandler(f"./logs/{file}")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

