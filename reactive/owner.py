from typing import Any, Callable

from .property import ReactiveProperty


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
