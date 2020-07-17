# ReactivePy

A simple library to manage reactive properties within an object using custom descriptors and update methods.

- [ReactivePy](#reactivepy)
  - [About ReactivePy](#about-reactivepy)
    - [`all_reactive` Decorator](#all_reactive-decorator)
    - [Using Type `bool`](#using-type-bool)
  - [`async` / `await` in ReactivePy](#async--await-in-reactivepy)

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

foo._bulk_update(name="Bar", age=12)
```

Reactive properties can also be strong-typed raising a `TypeError` if the value they're being set to doesn't match the `field_type` defined in the constructor. Strong-typing a property looks like this:

```python
class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = ReactiveProperty("Foo", field_type=str)
```

### `all_reactive` Decorator

The `ReactiveOwner.all_reactive` owner can be used on classes, where all public attributes should be reactive, which will additionally override the `__setattr__` method to convert any attribute writes.

```python
from reactive import all_reactive, ReactiveOwner

@all_reactive
class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = "Foo"
```

Additionally the parameters `only_type` and `not_type` can be specified, as a single type, list or tuple of types which will have only those types converted to `class ReactiveProperty` or not.

### Using Type `bool`

Since the type `bool` cannot be used as a base class, when retrieving its value, users must explicitly use `ReactiveProperty.value` attribute:

```python
from reactive import ReactiveOwner, ReactiveProperty

class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.boolean = ReactiveProperty(True)

foo = Foo()
print(foo.boolean.value)

>>> True
```

## `async` / `await` in ReactivePy

Oftentimes reactive models get updated from an external API source in which case it makes sense to use asynchronous programming to avoid the main program from being blocked by network requests. ReactivePy supports the `async`/`await` syntax by offering a `_async_bulk_update()` function, with an equivalent signature to `_bulk_update`, but will also call coroutine callbacks.

Reactive properties cannot async change callbacks, but this can be compensated for by supplying the properties a callback should respond to by adding it as an argument to `on_change`:

```python
from reactive import ReactiveOwner, ReactiveProperty

class Foo(ReactiveOwner):
    def __init__(self):
        super().__init__()
        self.name = ReactiveProperty("Foo")
        self.age = ReactiveProperty(6)

foo = Foo()

async def on_change(*args):
    for arg in args: print(arg.name, "updated to", arg.value)

async def on_name_change(*args):
    print("Name updated from", args[0].history[-1], "to", args[0].value)

foo.on_change(on_update, foo.name, foo.age)
foo.on_change(on_name_update, foo.name)

foo._async_bulk_update(name="Bar", age=12)
```
