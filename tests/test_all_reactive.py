import unittest
from typing import Any
from unittest import TestCase

import reactive


class TestAllReactive(TestCase):

    def test_1_all_reactive(self):
        @reactive.all_reactive
        class AllReactiveTestClass:
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute = "Test"
        all_reactive._private_attribute = "Test"
        self.assertTrue(hasattr(all_reactive.attribute, "on_change"))
        self.assertFalse(hasattr(all_reactive._private_attribute, "on_change"))

    def test_1_all_reactive_only_type(self):
        @reactive.all_reactive(not_type=[bool])
        class AllReactiveTestClass:
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))

    def test_1_all_reactive_not_type(self):
        @reactive.all_reactive(only_type=[str])
        class AllReactiveTestClass:
            pass

        all_reactive = AllReactiveTestClass()
        all_reactive.attribute_1 = "Test"
        all_reactive.attribute_2 = True
        self.assertTrue(hasattr(all_reactive.attribute_1, "on_change"))
        self.assertFalse(hasattr(all_reactive.attribute_2, "on_change"))


if __name__ == '__main__':
    unittest.main()
