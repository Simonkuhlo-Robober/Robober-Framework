import asyncio
from typing import Coroutine, Any


class AsyncTask:
    def __init__(self, target:Coroutine[Any, Any, Any], name:str | None = None) -> None:
        self.name:str = name
        self.target: Coroutine[Any, Any, Any] = target
        self.task: asyncio.Task | None = None