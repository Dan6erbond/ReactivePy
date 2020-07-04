from typing import Any

from reactive import ReactiveOwner, ReactiveProperty


class TestReactive:
    def test_change_joined(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        change_name_joined_called = False
        change_age_joined_called = False

        def call_change_joined(*args):
            nonlocal change_name_joined_called
            nonlocal change_age_joined_called

            for val in args:
                if val.name == "name":
                    change_name_joined_called = True
                elif val.name == "age":
                    change_age_joined_called = True

        foo = Foo()

        foo.on_change(call_change_joined, foo.name, foo.age)

        foo.name = "Bar"
        foo.age = 12

        assert change_name_joined_called
        assert change_age_joined_called

    def test_change_unique(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")

        change_name_unique_called = False

        def call_change_name(curr: Any, old: Any):
            nonlocal change_name_unique_called
            print(curr)
            change_name_unique_called = True

        foo = Foo()

        foo.name.on_change(call_change_name)

        foo.name = "Bar"

        assert change_name_unique_called

    def test_bulk_update(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        foo = Foo()

        def call_change_joined(*args):
            names = [arg.name for arg in args]
            assert ["name", "age"] == names

        foo.on_change(call_change_joined, foo.name, foo.age)

        foo._bulk_update({"name": "name", "value": "Bar"},
                         {"name": "age", "value": 12})
