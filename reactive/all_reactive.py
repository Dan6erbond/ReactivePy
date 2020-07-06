from typing import Any

from .owner import ReactiveOwner
from .property import ReactiveProperty


def to_tuple(val):
    if isinstance(val, list):
        return tuple(val)
    elif isinstance(val, tuple):
        return val
    elif val is None:
        return val
    else:
        return (val)


def make_all_reactive(org_cls=None, only_type=None, not_type=None):
    class AllReactive(org_cls, ReactiveOwner):
        def __init__(self):
            super().__init__()
            self.__doc__ = org_cls.__doc__
            self.__name__ = org_cls.__name__
            self.__only_type = to_tuple(only_type)
            self.__not_type = to_tuple(not_type)

        def __setattr__(self, name: str, value: Any):
            if not isinstance(value, ReactiveProperty) and not name.startswith("_"):
                if self.__only_type and not isinstance(value, self.__only_type):
                    return super().__setattr__(name, value)
                if self.__not_type and isinstance(value, self.__not_type):
                    return super().__setattr__(name, value)
                try:
                    value = ReactiveProperty(value, name)
                except TypeError:
                    pass
            return super().__setattr__(name, value)
    return AllReactive


def all_reactive(org_cls=None, only_type=None, not_type=None):
    if org_cls:
        return make_all_reactive(org_cls, only_type, not_type)
    else:
        def all_reactive_wrapper(org_cls):
            return make_all_reactive(org_cls, only_type, not_type)
        return all_reactive_wrapper
