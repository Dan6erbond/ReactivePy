from typing import Any, Callable


class ReactiveProperty:
    def __init__(self, value: Any, name: str = None):
        self.value = value
        self.name = name
        self.history = [value]
        self._on_change_handlers = []

    def __get__(self, instance: Any, owner: Any):
        class ObservableProperty(type(self.value)):
            name = self.name
            history = self.history
            on_change = self.on_change

        return ObservableProperty(self.value)

    def __set__(self, instance: Any, value: Any):
        prev = self.value
        self.value = value
        if value != prev:
            for change_handler in self._on_change_handlers:
                change_handler(self.value, prev)

    def __delete__(self, instance: Any):
        del self.value

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def on_change(self, func: Callable[[Any, Any], None]):
        self._on_change_handlers.append(func)
