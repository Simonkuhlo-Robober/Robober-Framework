from ..log_message import LogMessage

class SaveStrategy:
    filters:list = []
    def save(self, content:list[LogMessage]):
        pass