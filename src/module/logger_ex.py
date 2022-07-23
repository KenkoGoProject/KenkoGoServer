import json
import logging
import traceback
from logging import Formatter

from rich.logging import RichHandler

from module.server_status import ServerStatus


class LogLevel(int):
    CRITICAL = logging.CRITICAL  # 50
    FATAL = CRITICAL
    ERROR = logging.ERROR  # 40
    WARNING = logging.WARNING  # 30
    INFO = logging.INFO  # 20
    DEBUG = logging.DEBUG  # 10
    TRACE = 5
    NOTSET = logging.NOTSET  # 0


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, _object):
        if isinstance(_object, ServerStatus):
            return {
                'code': _object.value,
                'name': _object.name
            }
        return json.JSONEncoder.default(self, _object)


class LoggerEx:
    def __init__(self, name: str = None, log_level: int = LogLevel.INFO, show_name: bool = True):
        self.name = traceback.extract_stack()[-2].name if name is None else name
        self.show_name = show_name
        self.logger = logging.getLogger(self.name)

        rich_handler = RichHandler(show_time=False, show_path=False, rich_tracebacks=True, tracebacks_show_locals=True)
        fmt_string = '%(asctime)s.%(msecs)03d '
        if show_name:
            fmt_string += f'[{self.name}] '
        fmt_string += '%(message)s'
        rich_handler.setFormatter(Formatter(fmt=fmt_string, datefmt='%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(rich_handler)
        self.logger.setLevel(log_level)

    def set_level(self, level: int):
        self.logger.setLevel(level)

    def trace(self, *args, **kwargs):
        self.logger.log(LogLevel.TRACE, *args, **kwargs)

    def debug(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)


if __name__ == '__main__':

    def haha():
        log = LoggerEx(log_level=LogLevel.DEBUG)
        log.info("Hello, World!")
        log.critical("[blue underline]Hello, World!")
        log.debug("[blue underline]Hello, World!")
        log.warning("Hello, World!")
        log.error("Hello, World!")
        # log.trace("Hello, World!")

    haha()