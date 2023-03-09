import sys
import logging

from enum import Enum

class Color(Enum):
    GREEN = "\x1b[32;20m"
    RED = "\x1b[31;1m"
    YELLOW = "\x1b[33;20m"
    GREY = "\x1b[38;20m"
    RESET = "\x1b[0m"

class EmbedLoggerFormatter(logging.Formatter):
    format = "[%(asctime)s] %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: Color.GREY + format + Color.RESET,
        logging.INFO: Color.GREEN + format + Color.RESET,
        logging.WARNING: Color.YELLOW + format + Color.RESET,
        logging.ERROR: Color.RED + format + Color.RESET,
        logging.CRITICAL: Color.RED + format + Color.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class EmbedLogger(logging.getLoggerClass()):
    def __init__(self, name, verbose):
        super().__init__(name)

        self.setLevel(logging.DEBUG)
        logging.addLevelName(logging.INFO, 'FRAMEWORK')
        self.verbose = verbose

        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.setFormatter(EmbedLoggerFormatter)
        self.enable_console_output()

    def disable_console_output(self):
        if not self.has_console_handler():
            return
        self.removeHandler(self.stdout_handler)

    def enable_console_output(self):
        if self.has_console_handler():
            return
        self.addHandler(self.stdout_handler)

    def disable_file_output(self):
        if not self.has_file_handler():
            return
        self.removeHandler(self.file_handler)

    def enable_file_output(self):
        if self.has_file_handler():
            return
        self.addHandler(self.file_handler)

    def framework(self, msg, *args, **kwargs):
        return super().info(msg, *args, **kwargs)

    def _custom_log(self, func, msg, *args, **kwargs):
        if self.verbose:
            return func(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._custom_log(super().debug, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._custom_log(super().info, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._custom_log(super().warning, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._custom_log(super().error, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._custom_log(super().critical, msg, *args, **kwargs)