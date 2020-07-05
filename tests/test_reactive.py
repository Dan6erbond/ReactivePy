import unittest
from typing import Any
from unittest import TestCase

from reactive import ReactiveOwner, ReactiveProperty


class TestReactive(TestCase):
    def setUp(self):
        class TestClass(ReactiveOwner):
            def __init__(self):
                super().__init__()
                self.name = ReactiveProperty("Foo")
                self.age = ReactiveProperty(6)

        self.test_class = TestClass()
        self.test_class_2 = TestClass()

    def test_1_change_joined(self):
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

        self.test_class.on_change(call_change_joined, self.test_class.name, self.test_class.age)

        self.test_class.name = "Bar"
        self.test_class.age = 12

        self.test_class.name = "Bar"
        self.test_class.age = 12

        self.assertEqual(change_name_joined_called, 1)
        self.assertEqual(change_age_joined_called, 1)

    def test_2_change_any(self):
        change_any_called = 0

        def call_change_any(*args):
            nonlocal change_any_called
            change_any_called += 1

        self.test_class.on_change(call_change_any)

        self.test_class.name = "Bar"
        self.test_class.age = 12

        self.assertEqual(change_any_called, 2)

    def test_3_change_unique(self):
        change_name_unique_called = 0

        def call_change_name(curr: Any, prev: Any):
            nonlocal change_name_unique_called
            change_name_unique_called += 1

        self.test_class.name.on_change(call_change_name)

        self.test_class.name = "Bar"
        self.test_class.name = "Bar"

        self.assertEqual(change_name_unique_called, 1)

    def test_4_bulk_update(self):
        def call_change_joined(*args):
            names = [arg.name for arg in args]
            self.assertListEqual(["name", "age"], names)

        self.test_class.on_change(call_change_joined, self.test_class.name, self.test_class.age)

        self.test_class._bulk_update({"name": "name", "value": "Bar"},
                                     {"name": "age", "value": 12})

    def test_5_multiple_property_change_handlers(self):
        change_handler_1_calls = 0
        change_handler_2_calls = 0

        def change_handler_1(curr: Any, prev: Any):
            nonlocal change_handler_1_calls
            change_handler_1_calls += 1

        def change_handler_2(curr: Any, prev: Any):
            nonlocal change_handler_2_calls
            change_handler_2_calls += 1

        self.test_class.name.on_change(change_handler_1)
        self.test_class.name.on_change(change_handler_2)

        self.test_class.name = "Bar"

        self.assertEqual(change_handler_1_calls, 1)
        self.assertEqual(change_handler_2_calls, 1)

    def test_6_multiple_instances(self):
        self.test_class.name = "Bar"
        self.test_class_2.name = "Foo"

        self.assertEqual(self.test_class.name, "Bar")
        self.assertEqual(self.test_class_2.name, "Foo")

    def test_7_field_type(self):
        self.test_class.attribute = ReactiveProperty(True, field_type=bool)

        msg = "expected an instance of type 'bool' for attribute 'attribute', got 'int' instead"
        with self.assertRaises(TypeError, msg=msg):
            self.test_class.attribute = 12


if __name__ == '__main__':
    unittest.main()
