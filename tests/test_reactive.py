from typing import Any

from reactive import ReactiveOwner, ReactiveProperty


class TestReactive:
    def test_update_joined(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        update_name_joined_called = False
        update_age_joined_called = False

        def call_update_joined(val: Any):
            nonlocal update_name_joined_called
            nonlocal update_age_joined_called

            if val.name == "name":
                update_name_joined_called = True
            elif val.name == "age":
                update_age_joined_called = True

        foo = Foo()

        foo.on_update(call_update_joined, foo.name, foo.age)

        foo.name = "Bar"
        foo.age = 12

        assert update_name_joined_called
        assert update_age_joined_called

    def test_update_unique(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")

        update_name_unique_called = False

        def call_update_name(curr: Any, old: Any):
            nonlocal update_name_unique_called
            update_name_unique_called = True

        foo = Foo()

        foo.name.on_update(call_update_name)

        foo.name = "Bar"

        assert update_name_unique_called
