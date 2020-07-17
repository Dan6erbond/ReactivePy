import unittest
from typing import Any
from unittest import IsolatedAsyncioTestCase

from reactive import ReactiveOwner, ReactiveProperty


class TestReactive(IsolatedAsyncioTestCase):

    def setUp(self):
        class TestClass(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)
                self.boolean = ReactiveProperty(True)

        self.test_class = TestClass()

    async def test_1_async_change_joined(self):
        change_name_joined_called = 0
        change_age_joined_called = 0

        async def call_change_joined(*args):
            nonlocal change_name_joined_called
            nonlocal change_age_joined_called

            for val in args:
                if val.name == "name":
                    change_name_joined_called += 1
                elif val.name == "age":
                    change_age_joined_called += 1

        self.test_class.on_change(call_change_joined, self.test_class.name, self.test_class.age)

        await self.test_class._async_bulk_update(name="Bar", age=12)
        await self.test_class._async_bulk_update(name="Bar", age=12)

        self.assertEqual(change_name_joined_called, 1)
        self.assertEqual(change_age_joined_called, 1)

    async def test_2_async_change_any(self):
        change_any_called = 0

        async def call_change_any(*args):
            nonlocal change_any_called
            change_any_called += 1

        self.test_class.on_change(call_change_any)

        await self.test_class._async_bulk_update(name="Bar")
        await self.test_class._async_bulk_update(age=12)

        self.assertEqual(change_any_called, 2)

    async def test_3_async_bulk_update(self):
        async def call_change_joined(*args):
            names = [arg.name for arg in args]
            self.assertListEqual(["name", "age"], names)

        self.test_class.on_change(call_change_joined, self.test_class.name, self.test_class.age)

        self.assertTrue(await self.test_class._async_bulk_update(name="Bar", age=12))
        self.assertFalse(await self.test_class._async_bulk_update(name="Bar"))


if __name__ == '__main__':
    unittest.main()
