from reactive import ReactiveOwner, ReactiveProperty


class TestReactive:
    def test_reactive(self):
        class Foo(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)
                self.is_reactive = ReactiveProperty(True)

        foo = Foo()
        foo.on_update(
            lambda x: print(
                "Updated value:",
                x.name,
                "To:",
                x),
            foo.name,
            foo.age)
        foo.name.on_update(lambda x, y: print("New value:", x))
        foo.name = "Bar"
        foo.age = 12
