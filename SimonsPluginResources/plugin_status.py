import enum

class Status(enum.Enum):
    NOT_STARTED = 0
    STARTED = 1
    STOPPED = 2
    ERROR = 3