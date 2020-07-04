from typing import Any, List, Callable


class ReactiveProperty:
    def __init__(self, value: Any):
        self.value = value
        self.name = None
        self.history = [value]
        self._on_update = None

    def __get__(self, instance: Any, owner: Any):
        class ObservableProperty(type(self.value)):
            name = self.name
            history = self.history
            on_update = self.on_update
        return ObservableProperty(self.value)

    def __set__(self, instance: Any, value: Any):
        self.value = value
        if self._on_update:
            self._on_update(self.value, self.history[len(self.history) - 2])

    def __delete__(self, instance: Any):
        del self.value

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def on_update(self, func: Callable[[Any, Any], None]):
        self._on_update = func


class ReactiveOwner:
    def __init__(self):
        self._on_updates = []

    def on_update(self, func: Callable[..., None], *args):
        self._on_updates.append(
            (func, [object.__getattribute__(self, arg.name) for arg in args]))

    def __getattribute__(self, name: str):
        obj = object.__getattribute__(self, name)
        if hasattr(obj, '__get__'):
            return obj.__get__(self, type(self))
        return obj

    def __setattr__(self, name: str, value: Any):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            object.__setattr__(self, name, value)
        else:
            if hasattr(obj, '__set__'):
                print(True)
                obj.__set__(self, value)
                obj.__set_name__(self, name)
                print(obj)

                if isinstance(obj, ReactiveProperty):
                    print(True)
                    for update in self._on_updates:
                        if obj in update[1]:
                            update[0](obj)
            else:
                object.__setattr__(self, name, value)


class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = ReactiveProperty("Foo")
        self.age = ReactiveProperty(6)
        self.is_reactive = ReactiveProperty(True)


foo = Foo()
foo.on_update(
    lambda x: print(
        "Updated value:",
        x.name,
        "To:",
        x),
    foo.name,
    foo.age)
foo.name.on_update(lambda x, y: print("New value:", x))
foo.name = "Bar"
foo.age = 12
