# -*- coding: utf-8 -*-
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.meta import Meta
from pygerber.validators import CallOnCondition
from pygerber.validators.validator import Validator


class TestConditional(TestCase):
    def get_dummy_token(self):
        return SimpleNamespace(meta=Meta())

    def raise_ValueError(self):
        raise ValueError("Raised for testing purposes.")

    def test_conditional_succeed(self):
        token = self.get_dummy_token()
        validator = CallOnCondition(
            Validator(3),
            lambda token, value: True,
            lambda token, _: self.raise_ValueError(),
        )
        self.assertRaises(ValueError, validator, token, "foo")

    def test_conditional_fails(self):
        token = self.get_dummy_token()
        validator = CallOnCondition(
            Validator(3),
            lambda token, value: False,
            lambda token, _: self.raise_ValueError(),
        )
        self.assertEqual(validator(token, "foo"), 'foo')


if __name__ == "__main__":
    main()
