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

    def log(self, message:str, level: LogLevel | None = None) -> None:
        if level is None:
            level = self.default_level
        log_message = LogMessage(datetime.now().timestamp(), self.source, level, message)
        self.logger.log(log_message)