from typing import Any, Callable

from .property import ReactiveProperty


class ReactiveOwner:
    def __init__(self):
        self._on_changes = []

    def on_change(self, func: Callable[..., None], *args):
        self._on_changes.append((func, [object.__getattribute__(self, arg.name) for arg in args]))

    def __getattribute__(self, name: str):
        obj = object.__getattribute__(self, name)
        if hasattr(obj, '__get__'):
            return obj.__get__(self, type(self))
        return obj

    def _bulk_update(self, *args):
        funccalls = {}

        for arg in args:
            try:
                obj = object.__getattribute__(self, arg["name"])
            except AttributeError:
                object.__setattr__(self, arg["name"], arg["value"])
            else:
                if hasattr(obj, '__set__'):
                    prev = obj
                    obj.__set__(self, arg["value"])

                    if isinstance(obj, ReactiveProperty):
                        for change in self._on_changes:
                            if prev != obj and (obj in change[1] or not change[1]):
                                func = change[0]
                                if func in funccalls:
                                    funccalls[func] = funccalls[func] + [obj]
                                else:
                                    funccalls[func] = [obj]
                else:
                    object.__setattr__(self, arg["name"], arg["value"])

        for func in funccalls:
            func(*funccalls[func])

    def __setattr__(self, name: str, value: Any):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            object.__setattr__(self, name, value)
            if hasattr(value, '__set_name__'):
                value.__set_name__(self, name)
        else:
            if hasattr(obj, '__set__'):
                prev = obj.value
                obj.__set__(self, value)

                if isinstance(obj, ReactiveProperty):
                    for change in self._on_changes:
                        if prev != obj and (obj in change[1] or not change[1]):
                            change[0](*[obj])
            else:
                object.__setattr__(self, name, value)
