# ReactivePy

A simple library to manage reactive properties within an object using custom descriptors and update methods.

## About ReactivePy

ReactivePy lets you create objects that contain reactive properties. Those can be updated in bulk, which allows ReactivePy to notify its observers of changes. The callback can then read the history, update value as well as the name of the attribute.

```python
from reactive import ReactiveOwner, ReactiveProperty

class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = ReactiveProperty("Foo")
        self.age = ReactiveProperty(6)

foo = Foo()

def on_change(*args):
    for arg in args: print(arg.name, "updated to", arg)

def on_name_change(curr: Any, org: Any):
    print("Name updated from", org, "to", curr)

foo.on_change(on_update, foo.name, foo.age)
foo.name.on_change(on_name_update)

foo._bulk_update({"name": "name", "value": "Bar"},
                  {"name": "age", "value": 12})
```

Reactive properties can also be strong-typed raising a `TypeError` if the value they're being set to doesn't match the `field_type` defined in the constructor. Strong-typing a property looks like this:

```python
class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = ReactiveProperty("Foo", field_type=str)
```
