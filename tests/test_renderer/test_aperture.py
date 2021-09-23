# -*- coding: utf-8 -*-
from tests.testutils.renderer import get_filled_renderer
from tests.testutils.apertures import (
    CircleApertureCollector,
    PolygonApertureCollector,
    RectangleApertureCollector,
    get_dummy_apertureSet,
)
from pygerber.renderer.aperture_manager import ApertureManager
from types import SimpleNamespace
from unittest import TestCase, main
from unittest.mock import Mock

from pygerber.renderer.aperture import (
    Aperture,
    RegionApertureManager,
)
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.renderer.spec import ArcSpec, LineSpec


class ABCsTest(TestCase):
    def test_aperture(self):
        self.assertRaises(TypeError, Aperture)
        self.assertRaises(TypeError, lambda: Aperture.__init__(None, None, None))
        self.assertRaises(TypeError, lambda: Aperture.flash(None, None))
        self.assertRaises(TypeError, lambda: Aperture.line(None, None))
        self.assertRaises(TypeError, lambda: Aperture.arc(None, None))
        self.assertRaises(TypeError, lambda: Aperture.bbox(None))

    def test_aperture_bbox(self):
        mock = Mock()
        mock.bbox = Mock(return_value=BoundingBox(-0.5, 0.5, 0.5, -0.5))
        mock.DIAMETER = 1
        self.assertEqual(
            Aperture.arc_bbox(
                mock, ArcSpec(Vector2D(0, 0), Vector2D(1, 1), Vector2D(1, 0), False)
            ),
            BoundingBox(-0.5, 1.5, 2.5, -1.5),
        )

    def test_region(self):
        self.assertRaises(TypeError, RegionApertureManager)
        self.assertRaises(TypeError, RegionApertureManager.finish, None, None)

    def test_region_bbox(self):
        self.assertEqual(RegionApertureManager.bbox(None, []), BoundingBox(0, 0, 0, 0))
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertEqual(
            RegionApertureManager.bbox(
                None,
                [
                    LineSpec(Vector2D(0, 0), Vector2D(1, 1), True),
                ],
            ),
            BoundingBox(0, 1, 1, 0),
        )

    def test_region_bbox_many_bounds(self):
        self.assertEqual(RegionApertureManager.bbox(None, []), BoundingBox(0, 0, 0, 0))
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertEqual(
            RegionApertureManager.bbox(
                None,
                [
                    LineSpec(Vector2D(0, 0), Vector2D(1, 1), True),
                    LineSpec(Vector2D(1, 1), Vector2D(2, 2), True),
                ],
            ),
            BoundingBox(0, 2, 1, 2),
        )


class RectangularApertureTest(TestCase):
    def create_rectangle_aperture(
        self,
        args=SimpleNamespace(
            X=0.9,
            Y=0.23,
            HOLE_DIAMETER=0.1,
        ),
    ):
        return RectangleApertureCollector(
            args, ApertureManager(get_dummy_apertureSet(), None)
        )

    def test_create(self):
        aperture = self.create_rectangle_aperture()
        self.assertEqual(aperture.X, 0.9)
        self.assertEqual(aperture.Y, 0.23)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)

    def test_bbox(self):
        bbox = self.create_rectangle_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.45, 0.115, 0.45, -0.115))

    def test_line_bbox(self):
        bbox = self.create_rectangle_aperture().line_bbox(
            LineSpec(Vector2D(0, 0), Vector2D(2, 3), False),
        )
        self.assertEqual(bbox.as_tuple(), (-0.45, 3.115, 2.45, -0.115))

    def test_arc_bbox(self):
        bbox = self.create_rectangle_aperture().line_bbox(
            ArcSpec(Vector2D(0, 0), Vector2D(1, 1), Vector2D(1, 0), False),
        )
        self.assertEqual(bbox.as_tuple(), (-0.45, 1.115, 1.45, -0.115))


class CircularApertureTest(TestCase):
    def create_circle_aperture(
        self,
        args=SimpleNamespace(
            DIAMETER=0.6,
            HOLE_DIAMETER=0.1,
        ),
    ):
        return CircleApertureCollector(args, ApertureManager(get_dummy_apertureSet(), None))

    def test_create(self):
        aperture = self.create_circle_aperture()
        self.assertEqual(aperture.DIAMETER, 0.6)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)

    def test_bbox(self):
        bbox = self.create_circle_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.3, 0.3, 0.3, -0.3))


class PolygonApertureTest(TestCase):
    def create_polygon_aperture(
        self,
        args=SimpleNamespace(DIAMETER=0.6, HOLE_DIAMETER=0.1, ROTATION=0.3, VERTICES=5),
    ):
        return PolygonApertureCollector(args, ApertureManager(get_dummy_apertureSet(), None))

    def test_create(self):
        aperture = self.create_polygon_aperture()
        self.assertEqual(aperture.DIAMETER, 0.6)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)
        self.assertEqual(aperture.ROTATION, 0.3)
        self.assertEqual(aperture.VERTICES, 5)

    def test_bbox(self):
        bbox = self.create_polygon_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.3, 0.3, 0.3, -0.3))


if __name__ == "__main__":
    main()
