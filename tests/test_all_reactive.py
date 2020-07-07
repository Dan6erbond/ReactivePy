import unittest
from typing import Any
from unittest import TestCase

import reactive
from reactive import ReactiveOwner


class TestAllReactive(TestCase):

    def test_1_all_reactive(self):
        @reactive.all_reactive
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute = "Test"
        all_reactive._private_attribute = "Test"
        self.assertTrue(hasattr(all_reactive.attribute, "on_change"))
        self.assertFalse(hasattr(all_reactive._private_attribute, "on_change"))

    def test_2_all_reactive_doc(self):
        @reactive.all_reactive
        class AllReactiveTestClass(ReactiveOwner):
            """Test doc."""
            pass

        all_reactive = AllReactiveTestClass()
        self.assertEqual(all_reactive.__doc__, "Test doc.")

    def test_3_all_reactive_name(self):
        @reactive.all_reactive
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        self.assertEqual(all_reactive.__class__.__name__, "AllReactiveTestClass")

    def test_4_all_reactive_only_type_list(self):
        @reactive.all_reactive(not_type=[bool])
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))

    def test_5_all_reactive_only_type_tuple(self):
        @reactive.all_reactive(not_type=(bool))
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))

    def test_6_all_reactive_only_type_single_type(self):
        @reactive.all_reactive(not_type=bool)
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))

    def test_7_all_reactive_not_type(self):
        @reactive.all_reactive(only_type=[str])
        class AllReactiveTestClass(ReactiveOwner):
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))

    def test_8_all_reactive_init(self):
        @reactive.all_reactive(only_type=[str])
        class AllReactiveTestClass(ReactiveOwner):
            def __init__(self, arg1):
                assert arg1 == "arg1"

        all_reactive = AllReactiveTestClass("arg1")


if __name__ == '__main__':
    unittest.main()
