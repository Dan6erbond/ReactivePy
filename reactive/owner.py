from typing import Any, Callable

from .property import ReactiveProperty


def all_reactive(org_cls=None, only_type=None, not_type=None):
    if org_cls:
        class AllReactive(org_cls, ReactiveOwner):
            def __init__(self):
                super().__init__()
                self._only_type = only_type
                self._not_type = not_type

            def __setattr__(self, name: str, value: Any):
                if not isinstance(value, ReactiveProperty) and not name.startswith("_"):
                    if self._only_type and not isinstance(value, self._only_type):
                        return super().__setattr__(name, value)
                    if self._not_type and isinstance(value, self._not_type):
                        return super().__setattr__(name, value)
                    try:
                        value = ReactiveProperty(value, name)
                    except TypeError:
                        pass
                return super().__setattr__(name, value)

        return AllReactive

    def all_reactive_wrapper(org_cls):
        class AllReactive(org_cls, ReactiveOwner):
            def __init__(self):
                super().__init__()
                self._only_type = tuple(only_type) if only_type else only_type
                self._not_type = tuple(not_type) if not_type else not_type

            def __setattr__(self, name: str, value: Any):
                if not isinstance(value, ReactiveProperty) and not name.startswith("_"):
                    if self._only_type and not isinstance(value, self._only_type):
                        return super().__setattr__(name, value)
                    if self._not_type and isinstance(value, self._not_type):
                        return super().__setattr__(name, value)
                    try:
                        value = ReactiveProperty(value, name)
                    except TypeError:
                        pass
                return super().__setattr__(name, value)

        return AllReactive

    return all_reactive_wrapper


class ReactiveOwner:
    def __init__(self):
        self._on_change_handlers = []

    def on_change(self, func: Callable[..., None], *args):
        self._on_change_handlers.append((func, [object.__getattribute__(self, arg.name) for arg in args]))

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
                if hasattr(arg["value"], '__set_name__'):
                    arg["value"].__set_name__(self, arg["name"])
            else:
                if hasattr(obj, '__set__'):
                    if isinstance(obj, ReactiveProperty):
                        prev_value = obj.value
                    obj.__set__(self, arg["value"])

                    if isinstance(obj, ReactiveProperty):
                        for change_handler in self._on_change_handlers:
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

    def __setattr__(self, name: str, value: Any):
        return self._bulk_update({"name": name, "value": value})
