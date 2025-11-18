import asyncio
from typing import Coroutine, Any


from typing import Any, Callable
import asyncio

class AsyncTask:
    def __init__(
        self,
        target: Callable[..., Any],  # Function, not coroutine object!
        args: tuple = (),
        kwargs: dict = {},
        name: str | None = None,
    ) -> None:
        self.name = name
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.task: asyncio.Task | None = None