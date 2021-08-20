# -*- coding: utf-8 -*-
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.meta.aperture import (
    Aperture,
    CircularAperture,
    PolygonAperture,
    RectangularAperture,
)


class TestRectangleAperture(RectangularAperture):
    def flash(self) -> None:
        pass

    def line(self) -> None:
        pass

    def arc(self) -> None:
        pass


class TestCircleAperture(CircularAperture):
    def flash(self) -> None:
        pass

    def line(self) -> None:
        pass

    def arc(self) -> None:
        pass


class TestPolygonAperture(PolygonAperture):
    def flash(self) -> None:
        pass

    def line(self) -> None:
        pass

    def arc(self) -> None:
        pass


class RectangularApertureTest(TestCase):
    def create_rectangle_aperture(
        self,
        args=SimpleNamespace(
            X=0.9,
            Y=0.23,
            HOLE_DIAMETER=0.1,
        ),
    ):
        return TestRectangleAperture(args)

    def test_rectangle(self):
        aperture = self.create_rectangle_aperture()
        self.assertEqual(aperture.X, 0.9)
        self.assertEqual(aperture.Y, 0.23)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)

    def test_rectangle_bbox(self):
        bbox = self.create_rectangle_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.45, 0.115, 0.45, -0.115))


class CircularApertureTest(TestCase):
    def create_circle_aperture(
        self,
        args=SimpleNamespace(
            DIAMETER=0.6,
            HOLE_DIAMETER=0.1,
        ),
    ):
        return TestCircleAperture(args)

    def test_circle(self):
        aperture = self.create_circle_aperture()
        self.assertEqual(aperture.DIAMETER, 0.6)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)

    def test_circle_bbox(self):
        bbox = self.create_circle_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.3, 0.3, 0.3, -0.3))


class PolygonApertureTest(TestCase):
    def create_polygon_aperture(
        self,
        args=SimpleNamespace(
            DIAMETER=0.6,
            HOLE_DIAMETER=0.1,
            ROTATION=0.3,
            VERTICES=5
        ),
    ):
        return TestPolygonAperture(args)

    def test_polygon(self):
        aperture = self.create_polygon_aperture()
        self.assertEqual(aperture.DIAMETER, 0.6)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)
        self.assertEqual(aperture.ROTATION, 0.3)
        self.assertEqual(aperture.VERTICES, 5)

    def test_circle_bbox(self):
        bbox = self.create_polygon_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.3, 0.3, 0.3, -0.3))



if __name__ == "__main__":
    main()
