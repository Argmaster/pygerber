# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.drawing_state import DrawingState
from pygerber.validators.basic import Float, Function, Int, String


class BasicValidatorsTest(TestCase):
    def test_Float_validator(self):
        token = None
        state = DrawingState()
        default = 999.999
        validator = Float(default)
        self.assertEqual(validator(token, state, "3342.232"), 3342.232)
        self.assertEqual(validator(token, state, None), default)

    def test_Int_validator(self):
        token = None
        state = DrawingState()
        default = 242
        validator = Int(default)
        self.assertEqual(validator(token, state, "3342"), 3342)
        self.assertEqual(validator(token, state, None), default)

    def test_String_validator(self):
        token = None
        state = DrawingState()
        default = "some default"
        validator = String(default)
        test_value = "some string"
        self.assertEqual(validator(token, state, test_value), test_value)
        self.assertEqual(validator(token, state, None), default)

    def test_Function_validator(self):
        token = None
        state = DrawingState()
        default = "some default"
        validator = Function(lambda tk, value: default)
        self.assertEqual(validator(token, state, None), default)


if __name__ == "__main__":
    main()
