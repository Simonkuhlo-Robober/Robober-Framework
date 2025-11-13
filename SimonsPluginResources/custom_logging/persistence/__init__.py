from ..log_message import LogMessage
from res import SaveStrategy

save_strategies:list[SaveStrategy] = []
dynamic_saving:bool = False
cache_storage:list[LogMessage] = []

def cache(entry:LogMessage):
    global cache_storage
    cache_storage.append(entry)
    if dynamic_saving:
        for save_strategy in save_strategies:
            save_strategy.save([entry])

def save():
    for save_strategy in save_strategies:
        save_strategy.save(cache_storage)
    cache_storage.clear()