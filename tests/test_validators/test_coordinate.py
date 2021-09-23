# -*- coding: utf-8 -*-
from pygerber.drawing_state import DrawingState
from pygerber.mathclasses import Vector2D
from unittest.mock import Mock
from pygerber.validators.coordinate import Coordinate
from unittest import TestCase, main


class CoordinateTest(TestCase):

    def test_Coordinate(self):
        token = None
        state = DrawingState()
        test_value = "30100"
        validator = Coordinate()
        self.assertEqual(validator(token, state, test_value), 0.0301)
        self.assertRaises(TypeError, lambda: validator(token, None))


if __name__ == "__main__":
    main()
