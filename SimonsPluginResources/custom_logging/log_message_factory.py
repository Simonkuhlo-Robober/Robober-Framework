from .logger import Logger
from .log_message import LogMessage
from .loglevel import LogLevel, DefaultLogLevels
from .sources import LogMessageSource
from datetime import datetime

class LogMessageFactory:
    def __init__(self, logger:Logger, source: LogMessageSource = LogMessageSource(), default_level:LogLevel = DefaultLogLevels.INFO) -> None:
        self.logger = logger
        self.source = source
        self.default_level = default_level
        self.warn_level: LogLevel = DefaultLogLevels.WARNING
        self.error_level: LogLevel = DefaultLogLevels.ERROR
        self.debug_level: LogLevel = DefaultLogLevels.DEBUG
        self.info_level: LogLevel = DefaultLogLevels.INFO

    def log(self, message:str, level: LogLevel | None = None) -> None:
        if level is None:
            level = self.default_level
        log_message = LogMessage(datetime.now().timestamp(), self.source, level, message)
        self.logger.log(log_message)

    def info(self, message:str) -> None:
        log_message = LogMessage(datetime.now().timestamp(), self.source, self.info_level, message)
        self.logger.log(log_message)

    def warn(self, message:str) -> None:
        log_message = LogMessage(datetime.now().timestamp(), self.source, self.warn_level, message)
        self.logger.log(log_message)

    def error(self, message:str) -> None:
        log_message = LogMessage(datetime.now().timestamp(), self.source, self.error_level, message)
        self.logger.log(log_message)

    def debug(self, message:str) -> None:
        log_message = LogMessage(datetime.now().timestamp(), self.source, self.debug_level, message)
        self.logger.log(log_message)