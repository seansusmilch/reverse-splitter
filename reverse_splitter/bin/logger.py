import logging
import sys
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', logging.DEBUG) # can be string 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

def setup_logger(name:str):
    logFormatter = logging.Formatter(fmt='%(levelname)s - %(name)s - %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logFormatter)
    logger.addHandler(handler)
    return logger