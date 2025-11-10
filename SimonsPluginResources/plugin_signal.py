import threading
from inspect import signature
from typing import Callable, get_type_hints

class Signal:

    def __init__(self, **arg_types):
        self.arg_types = arg_types
        self.connected_handlers: list[Callable] = []
        self._lock = threading.Lock()

    def connect(self, handler: Callable):
        with self._lock:
            if handler in self.connected_handlers:
                return

            # Inspect function’s expected parameters and type hints
            sig = signature(handler)
            hints = get_type_hints(handler)

            # NOTE vvvv Delete candidate, might not be useful / wanted
            # To Validate argument count
            if len(sig.parameters) != len(self.arg_types):
                raise TypeError(f"{handler.__name__} has wrong number of arguments; expected {len(self.arg_types)}")
            # NOTE ^^^^

            # Validate argument names and types
            for (expected_name, expected_type), (param_name, param) in zip(self.arg_types.items(), sig.parameters.items()):
                # NOTE vvvv Delete candidate, might not be useful / wanted
                if expected_name != param_name:
                    raise TypeError(f"Expected argument '{expected_name}', got '{param_name}' in {handler.__name__}")
                # NOTE ^^^^
                if param_name in hints and not issubclass(hints[param_name], expected_type):
                    raise TypeError(f"Handler '{handler.__name__}' argument '{param_name}' must be of type {expected_type}")

            self.connected_handlers.append(handler)

    def disconnect(self, handler: Callable):
        with self._lock:
            if handler in self.connected_handlers:
                self.connected_handlers.remove(handler)

    def emit(self, *args, **kwargs):
        with self._lock:
            handlers = list(self.connected_handlers)
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"Signal handler {handler.__name__} raised {e}")