from typing import Any, Callable

from .property import ReactiveProperty


class ReactiveOwner:
    def __init__(self):
        self.__on_change_handlers = []

    def on_change(self, func: Callable[..., None], *args):
        self.__on_change_handlers.append((func, [object.__getattribute__(self, arg.name) for arg in args]))

    def __getattribute__(self, name: str):
        obj = object.__getattribute__(self, name)
        if hasattr(obj, '__get__'):
            return obj.__get__(self, type(self))
        return obj

    def _bulk_update(self, *args):
        changed = False
        funccalls = {}

        for arg in args:
            try:
                obj = object.__getattribute__(self, arg["name"])
            except AttributeError:
                object.__setattr__(self, arg["name"], arg["value"])
                if hasattr(arg["value"], '__set_name__'):
                    arg["value"].__set_name__(self, arg["name"])
            else:
                if hasattr(obj, '__set__'):
                    if isinstance(obj, ReactiveProperty):
                        prev_value = obj.value
                    obj.__set__(self, arg["value"])

                    if isinstance(obj, ReactiveProperty):
                        if prev_value != obj.value:
                            changed = True
                        for change_handler in self.__on_change_handlers:
                            if prev_value != obj.value and (obj in change_handler[1] or not change_handler[1]):
                                func = change_handler[0]
                                if func in funccalls:
                                    funccalls[func] = funccalls[func] + [obj]
                                else:
                                    funccalls[func] = [obj]
                else:
                    object.__setattr__(self, arg["name"], arg["value"])

        for func in funccalls:
            func(*funccalls[func])
        return changed

    def __setattr__(self, name: str, value: Any):
        return self._bulk_update({"name": name, "value": value})
