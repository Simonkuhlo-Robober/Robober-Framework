from termcolor import colored

def success(text:str) -> str:
    return green(text)

def highlight_positive(text:str) -> str:
    return text

def highlight_negative(text:str) -> str:
    return text

def highlight(text:str) -> str:
    return blue(text)

def blue(text:str) -> str:
    return colored(text, "blue")

def green(text:str) -> str:
    return colored(text, "green")

def red(text:str) -> str:
    return colored(text, "red")