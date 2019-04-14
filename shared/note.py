from logging import (
    DEBUG, ERROR, INFO, WARNING, Formatter, StreamHandler, getLogger
)
from logging.handlers import RotatingFileHandler
from os import path

LOG_LEVELS = dict(debug=DEBUG, error=ERROR, info=INFO, warning=WARNING)


def _setup_log_handler(handler, formatter, level):
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler


def log_setup(log_name, log_folder, log_level):
    root_log = getLogger()
    formatter = Formatter('''
%(levelname)s - %(asctime)s | %(name)s | %(processName)s %(threadName)s
%(module)s.%(funcName)s [%(pathname)s:%(lineno)d]
    %(message)s
    '''.rstrip())
    level = LOG_LEVELS.get(log_level, DEBUG)
    file_size = 10 * (1024 * 1024)

    root_log.setLevel(DEBUG)
    root_log.addHandler(_setup_log_handler(
        StreamHandler(stream=None),
        formatter, level
    ))
    root_log.addHandler(_setup_log_handler(
        RotatingFileHandler(
            path.join(log_folder, '{}_{}.log'.format(log_name, log_level)),
            maxBytes=file_size, backupCount=9
        ),
        formatter, level
    ))

    if level != DEBUG:
        root_log.addHandler(_setup_log_handler(
            RotatingFileHandler(
                path.join(log_folder, '{}_debug.log'.format(log_name)),
                maxBytes=file_size, backupCount=4
            ),
            formatter, DEBUG
        ))

    root_log.debug('=' * 80)
