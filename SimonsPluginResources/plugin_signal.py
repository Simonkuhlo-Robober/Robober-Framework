import asyncio
from inspect import signature, iscoroutinefunction
from typing import Callable, get_type_hints, Any

class Signal:

    def __init__(self, **arg_types: type):
        self.arg_types = arg_types
        self.connected_handlers: list[Callable[..., Any]] = []

    def connect(self, handler: Callable[..., Any]):
        if handler in self.connected_handlers:
            return

        sig = signature(handler)
        hints = get_type_hints(handler)

        # Validate parameter count
        if len(sig.parameters) != len(self.arg_types):
            raise TypeError(
                f"{handler.__name__} has wrong number of arguments; expected {len(self.arg_types)}"
            )

        # Validate parameter names and types
        for (expected_name, expected_type), (param_name, param) in zip(
            self.arg_types.items(), sig.parameters.items()
        ):
            if expected_name != param_name:
                raise TypeError(
                    f"Expected argument '{expected_name}', got '{param_name}' in {handler.__name__}"
                )
            if param_name in hints and not issubclass(hints[param_name], expected_type):
                raise TypeError(
                    f"Handler '{handler.__name__}' argument '{param_name}' must be of type {expected_type}"
                )

        self.connected_handlers.append(handler)

    def disconnect(self, handler: Callable[..., Any]):
        if handler in self.connected_handlers:
            self.connected_handlers.remove(handler)

    async def emit(self, *args: Any, **kwargs: Any):
        handlers = list(self.connected_handlers)
        tasks = []
        for handler in handlers:
            try:
                if iscoroutinefunction(handler):
                    tasks.append(asyncio.create_task(handler(*args, **kwargs)))
                else:
                    # Run sync functions in a thread pool
                    loop = asyncio.get_running_loop()
                    tasks.append(loop.run_in_executor(None, handler, *args, **kwargs))
            except Exception as e:
                print(f"Signal handler {handler.__name__} raised {e}")
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
