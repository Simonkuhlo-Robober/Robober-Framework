from dataclasses import dataclass

@dataclass(frozen=True)
class LogLevel:
    num: int
    label: str
    description: str

class DefaultLogLevels:
    DEBUG = LogLevel(1, "[DEBUG]", "Debugging")
    INFO = LogLevel(2, "[INFO]", "Information")
    WARNING = LogLevel(3, "[WARN]", "Warning")
    ERROR = LogLevel(4, "[ERROR]", "Error")