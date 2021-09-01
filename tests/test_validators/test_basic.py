# -*- coding: utf-8 -*-
from pygerber.validators.basic import Function
from unittest import TestCase, main
from pygerber.validators import Float, Int, String


class BasicValidatorsTest(TestCase):
    def test_Float_validator(self):
        token = None
        default = 999.999
        validator = Float(default)
        self.assertEqual(validator(token, "3342.232"), 3342.232)
        self.assertEqual(validator(token, None), default)

    def test_Int_validator(self):
        token = None
        default = 242
        validator = Int(default)
        self.assertEqual(validator(token, "3342"), 3342)
        self.assertEqual(validator(token, None), default)

    def test_String_validator(self):
        token = None
        default = "some default"
        validator = String(default)
        test_value = "some string"
        self.assertEqual(validator(token, test_value), test_value)
        self.assertEqual(validator(token, None), default)

    def test_Function_validator(self):
        token = None
        default = "some default"
        validator = Function(lambda tk, value: default)
        self.assertEqual(validator(token, None), default)


if __name__ == "__main__":
    main()
