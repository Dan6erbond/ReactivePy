from typing import Any

from reactive import ReactiveOwner, ReactiveProperty


class TestReactive:
    def test_change_joined(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        change_name_joined_called = 0
        change_age_joined_called = 0

        def call_change_joined(*args):
            nonlocal change_name_joined_called
            nonlocal change_age_joined_called

            for val in args:
                if val.name == "name":
                    change_name_joined_called += 1
                elif val.name == "age":
                    change_age_joined_called += 1

        foo = Foo()

        foo.on_change(call_change_joined, foo.name, foo.age)

        foo.name = "Bar"
        foo.age = 12

        foo.name = "Bar"
        foo.age = 12

        assert change_name_joined_called == 1
        assert change_age_joined_called == 1

    def test_change_any(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        change_any_called = 0

        def call_change_any(*args):
            nonlocal change_any_called
            change_any_called += 1

        foo = Foo()

        foo.on_change(call_change_any)

        foo.name = "Bar"
        foo.age = 12

        assert change_any_called == 2

    def test_change_unique(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")

        change_name_unique_called = 0

        def call_change_name(curr: Any, prev: Any):
            nonlocal change_name_unique_called
            change_name_unique_called += 1

        foo = Foo()

        foo.name.on_change(call_change_name)

        foo.name = "Bar"
        foo.name = "Bar"

        assert change_name_unique_called == 1

    def test_bulk_update(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        def call_change_joined(*args):
            names = [arg.name for arg in args]
            assert ["name", "age"] == names

        foo = Foo()

        foo.on_change(call_change_joined, foo.name, foo.age)

        foo._bulk_update({"name": "name", "value": "Bar"},
                         {"name": "age", "value": 12})

    def test_multiple_property_change_handlers(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")

        change_handler_1_calls = 0
        change_handler_2_calls = 0

        def change_handler_1(curr: Any, prev: Any):
            nonlocal change_handler_1_calls
            change_handler_1_calls += 1

        def change_handler_2(curr: Any, prev: Any):
            nonlocal change_handler_2_calls
            change_handler_2_calls += 1

        foo = Foo()

        foo.name.on_change(change_handler_1)
        foo.name.on_change(change_handler_2)

        foo.name = "Bar"

        assert change_handler_1_calls == 1
        assert change_handler_2_calls == 1
