# -*- coding: utf-8 -*-
from pygerber.exceptions import InvalidCommandFormat
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.validators import Dispatcher, load_validators
from pygerber.validators.validator import Validator


class DispatcherTest(TestCase):
    def get_dummy_token(self):
        return SimpleNamespace(meta=Meta(None))

    def test_dispatcher(self):
        token = self.get_dummy_token()

        class ARGS_dispatcher(Dispatcher):
            VALUE = Validator()

        validator1 = ARGS_dispatcher(r"(?P<VALUE>[a-z]+)")

        cleaned1 = validator1(token, "foo")
        cleaned2 = validator1(token, "bar")
        self.assertEqual(cleaned1.VALUE, "foo")
        self.assertEqual(cleaned2.VALUE, "bar")

    def test_dispatcher_fail(self):
        token = self.get_dummy_token()

        class ARGS_dispatcher(Dispatcher):
            VALUE = Validator()

        validator1 = ARGS_dispatcher(r"(?P<VALUE>[a-z]+)")

        self.assertRaises(InvalidCommandFormat, lambda: validator1(token, "346"))


if __name__ == "__main__":
    main()
