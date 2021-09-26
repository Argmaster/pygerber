# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from pygerber.mathclasses import BoundingBox
from pygerber.mathclasses import Vector2D
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec
from pygerber.renderer.spec import Spec


class SpecTest(TestCase):
    @staticmethod
    def get_aperture_mock() -> MagicMock:
        aperture_mock = MagicMock()
        aperture_mock.flash = MagicMock()
        aperture_mock.flash_bbox = MagicMock(return_value=BoundingBox(0, 0, 0, 0))
        aperture_mock.line = MagicMock()
        aperture_mock.line_bbox = MagicMock(return_value=BoundingBox(0, 0, 0, 0))
        aperture_mock.arc = MagicMock()
        aperture_mock.arc_bbox = MagicMock(return_value=BoundingBox(0, 0, 0, 0))
        return aperture_mock

    def test_spec(self):
        self.assertRaises(TypeError, Spec)
        self.assertRaises(TypeError, Spec.draw, None, None)
        self.assertRaises(TypeError, Spec.bbox, None, None)

    def test_FlashSpec(self):
        location = Vector2D(332, 24)
        spec = FlashSpec(location, True)
        aperture_mock = self.get_aperture_mock()
        spec.draw(aperture_mock)
        self.assertEqual(aperture_mock.flash.call_args.args[0], spec)
        spec.bbox(aperture_mock)
        self.assertEqual(aperture_mock.flash.call_args.args[0], spec)

    def test_LineSpec(self):
        begin = Vector2D(3, 1)
        end = Vector2D(4, 122)
        spec = LineSpec(begin, end, False)
        self.assertEqual(spec.begin, begin)
        self.assertEqual(spec.end, end)
        self.assertEqual(spec.is_region, False)
        aperture_mock = self.get_aperture_mock()
        spec.draw(aperture_mock)
        self.assertEqual(aperture_mock.line.call_args.args[0], spec)
        spec.bbox(aperture_mock)
        self.assertEqual(aperture_mock.line_bbox.call_args.args[0], spec)

    def test_ArcSpec(self):
        begin = Vector2D(-2, 1)
        end = Vector2D(1, 3)
        center = Vector2D(1, 1)
        spec = ArcSpec(begin, end, center, False)
        self.assertEqual(spec.begin, begin)
        self.assertEqual(spec.end, end)
        self.assertEqual(spec.center, center)
        self.assertEqual(spec.is_region, False)
        aperture_mock = self.get_aperture_mock()
        spec.draw(aperture_mock)
        self.assertEqual(aperture_mock.arc.call_args.args[0], spec)
        spec.bbox(aperture_mock)
        self.assertEqual(aperture_mock.arc_bbox.call_args.args[0], spec)


if __name__ == "__main__":
    main()
