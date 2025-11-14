from .sources import LogMessageSource
from .loglevel import LogLevel, DefaultLogLevels

class LogMessage:
    def __init__(self, timestamp: float, source: LogMessageSource = LogMessageSource(), level: LogLevel = DefaultLogLevels.INFO, message: str = ""):
        self.timestamp = timestamp
        self.source = source
        self.level = level
        self.message = message

    def __str__(self) -> str:
        output: str = f"{self.level.label} {self.source}: {self.message}"
        return output