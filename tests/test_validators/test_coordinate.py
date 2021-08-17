# -*- coding: utf-8 -*-
from types import SimpleNamespace
from unittest import TestCase, main
from pygerber.validators import Coordinate
from pygerber.meta import Meta


class CoordinateTest(TestCase):
    def get_dummy_token(self):
        return SimpleNamespace(meta=Meta())

    def test_coordinate(self):
        token = self.get_dummy_token()
        test_value = "30100"
        validator = Coordinate()
        self.assertEqual(validator(token, test_value), 0.0301)


if __name__ == "__main__":
    main()
