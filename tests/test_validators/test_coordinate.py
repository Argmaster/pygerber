# -*- coding: utf-8 -*-
from pygerber.mathclasses import Vector2D
from unittest.mock import Mock
from pygerber.validators.coordinate import Coordinate, VectorCoordinateX, VectorCoordinateY
from types import SimpleNamespace
from unittest import TestCase, main
from pygerber.meta import Meta


class CoordinateTest(TestCase):
    def get_dummy_token(self):
        return SimpleNamespace(
            meta=Meta(None),
            get_current_point=Mock(
                return_value=Vector2D(1, 2),
            ),
        )

    def test_Coordinate(self):
        token = self.get_dummy_token()
        test_value = "30100"
        validator = Coordinate()
        self.assertEqual(validator(token, test_value), 0.0301)
        self.assertRaises(TypeError, lambda: validator(token, None))

    def test_VectorCoordinateX(self):
        token = self.get_dummy_token()
        test_value = "30100"
        validator = VectorCoordinateX()
        self.assertEqual(validator(token, test_value), 0.0301)
        self.assertEqual(validator(token, None), 1)

    def test_VectorCoordinateY(self):
        token = self.get_dummy_token()
        test_value = "30100"
        validator = VectorCoordinateY()
        self.assertEqual(validator(token, test_value), 0.0301)
        self.assertEqual(validator(token, None), 2)


if __name__ == "__main__":
    main()
