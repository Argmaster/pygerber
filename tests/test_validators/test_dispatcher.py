# -*- coding: utf-8 -*-
from pygerber.drawing_state import DrawingState
from pygerber.exceptions import InvalidCommandFormat
from unittest import TestCase, main

from pygerber.validators.struct_validator import StructValidator
from pygerber.validators.validator import Validator


class DispatcherTest(TestCase):
    def test_dispatcher(self):
        class ARGS_dispatcher(StructValidator):
            VALUE = Validator()

        validator1 = ARGS_dispatcher(r"(?P<VALUE>[a-z]+)")

        cleaned1 = validator1(None, DrawingState(), "foo")
        cleaned2 = validator1(None, DrawingState(), "bar")
        self.assertEqual(cleaned1.VALUE, "foo")
        self.assertEqual(cleaned2.VALUE, "bar")

    def test_dispatcher_fail(self):
        class ARGS_dispatcher(StructValidator):
            VALUE = Validator()

        validator1 = ARGS_dispatcher(r"(?P<VALUE>[a-z]+)")

        self.assertRaises(
            InvalidCommandFormat, lambda: validator1(None, DrawingState(), "346")
        )


if __name__ == "__main__":
    main()
