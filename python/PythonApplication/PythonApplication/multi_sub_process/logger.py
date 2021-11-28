
import os
import logging

from logging.handlers import RotatingFileHandler


def get_logger(file_name):
    logger = logging.getLogger(__name__)

    os.makedirs('logs', exist_ok=True)
    log_file = os.path.join('logs', file_name)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    rHandler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=10)
    rFormatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s')
    rHandler.setFormatter(rFormatter)
    rHandler.setLevel(logging.DEBUG)
    logger.addHandler(rHandler)

    return logger
