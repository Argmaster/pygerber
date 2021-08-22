# -*- coding: utf-8 -*-
from unittest import TestCase, main

from pygerber.mathclasses import Vector2D
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec


class SpecTest(TestCase):
    def test_FlashSpec(self):
        location = Vector2D(332, 24)
        spec = FlashSpec(location, True)

    def test_LineSpec(self):
        begin = Vector2D(3, 1)
        end = Vector2D(4, 122)
        spec = LineSpec(begin, end, False)
        self.assertEqual(spec.begin, begin)
        self.assertEqual(spec.end, end)
        self.assertEqual(spec.is_region, False)

    def test_ArcSpec(self):
        begin = Vector2D(-2, 1)
        end = Vector2D(1, 3)
        center = Vector2D(1, 1)
        spec = ArcSpec(begin, end, center, False)
        self.assertEqual(spec.begin, begin)
        self.assertEqual(spec.end, end)
        self.assertEqual(spec.center, center)
        self.assertEqual(spec.is_region, False)


if __name__ == "__main__":
    main()
