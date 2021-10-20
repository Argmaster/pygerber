# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.drawing_state import DrawingState
from pygerber.validators.conditional import CallOnCondition
from pygerber.validators.validator import Validator


class TestConditional(TestCase):
    def test_conditional_succeed(self):
        def raise_ValueError():
            raise ValueError()

        token = None
        state = DrawingState()
        validator = CallOnCondition(
            Validator(3),
            lambda token, value: True,
            lambda token, _: raise_ValueError(),
        )
        self.assertRaises(ValueError, validator, token, state, "foo")

    def test_conditional_fails(self):
        token = None
        state = DrawingState()
        validator = CallOnCondition(
            Validator(3),
            lambda token, value: False,
            lambda token, _: self.raise_ValueError(),
        )
        self.assertEqual(validator(token, state, "foo"), "foo")


if __name__ == "__main__":
    main()
