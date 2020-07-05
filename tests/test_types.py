import unittest
from typing import Any
from unittest import TestCase

from reactive import ReactiveOwner, ReactiveProperty


class TestTypes(TestCase):
    def setUp(self):
        @ReactiveOwner.all_reactive
        class TestClass:
            pass

        self.test_class = TestClass()

    def test_1_integer(self):
        self.test_class.integer = 1
        self.assertEqual(self.test_class.integer, 1)

    def test_2_string(self):
        self.test_class.string = "Foo"
        self.assertEqual(self.test_class.string, "Foo")

    def test_3_boolean(self):
        self.test_class.boolean = True
        self.assertTrue(self.test_class.boolean)

    def test_4_callable(self):
        def func():
            pass

        msg = "type 'function' is invalid for the value of 'ReactiveProperty'."
        with self.assertRaises(TypeError, msg=msg):
            ReactiveProperty(func)

        self.test_class.func = func
        self.assertEqual(self.test_class.func.__name__, func.__name__)

    def test_5_async_callable(self):
        async def async_func():
            pass

        msg = "type 'function' is invalid for the value of 'ReactiveProperty'."
        with self.assertRaises(TypeError, msg=msg):
            ReactiveProperty(async_func)

        self.test_class.async_func = async_func
        self.assertEqual(self.test_class.async_func.__name__, async_func.__name__)


if __name__ == '__main__':
    unittest.main()
