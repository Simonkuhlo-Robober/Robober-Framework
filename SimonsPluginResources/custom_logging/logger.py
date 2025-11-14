from .log_message import LogMessage

class Logger:
    ## Prints a given Message and saves it to the log cache
    @staticmethod
    def log(msg:LogMessage):
        # TODO Cache / Save message
        print(msg)