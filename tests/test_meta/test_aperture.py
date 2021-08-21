# -*- coding: utf-8 -*-
from typing import List, Tuple
from pygerber.meta.data import Vector2D
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec, Spec
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.meta.aperture import (
    Aperture,
    ApertureSet,
    CircularAperture,
    PolygonAperture,
    RectangularAperture,
    RegionApertureManager,
)


class ApertureCollector:
    class Called(Exception):
        pass
    class CalledWithSpec(Exception):
        def __init__(self, spec: Spec) -> None:
            self.spec = spec

    class CalledFlash(CalledWithSpec):
        pass

    class CalledLine(CalledWithSpec):
        pass

    class CalledArc(CalledWithSpec):
        pass

    class CalledFinish(Called):
        def __init__(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
            self.bounds = bounds

    def flash(self, spec: FlashSpec) -> None:
        raise self.CalledFlash(spec)

    def line(self, spec: LineSpec) -> None:
        raise self.CalledLine(spec)

    def arc(self, spec: ArcSpec) -> None:
        raise self.CalledArc(spec)

    def finish(self, bounds: List[Tuple[Aperture, Spec]]) -> None:
        raise self.CalledFinish(bounds)


class RectangleApertureCollector(ApertureCollector, RectangularAperture):
    pass


class CircleApertureCollector(ApertureCollector, CircularAperture):
    pass


class PolygonApertureCollector(ApertureCollector, PolygonAperture):
    pass


class RegionApertureCollector(ApertureCollector, RegionApertureManager):
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
        return RectangleApertureCollector(args)

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
        return CircleApertureCollector(args)

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
        return PolygonApertureCollector(args)

    def test_create(self):
        aperture = self.create_polygon_aperture()
        self.assertEqual(aperture.DIAMETER, 0.6)
        self.assertEqual(aperture.HOLE_DIAMETER, 0.1)
        self.assertEqual(aperture.ROTATION, 0.3)
        self.assertEqual(aperture.VERTICES, 5)

    def test_bbox(self):
        bbox = self.create_polygon_aperture().bbox()
        self.assertEqual(bbox.as_tuple(), (-0.3, 0.3, 0.3, -0.3))


class ApertureSetTest(TestCase):
    @staticmethod
    def get_dummy_apertureSet():
        return ApertureSet(
            CircleApertureCollector,
            RectangleApertureCollector,
            RectangleApertureCollector,
            PolygonApertureCollector,
            RegionApertureCollector,
        )

    def test_getApertureClass(self):
        AS = self.get_dummy_apertureSet()
        self.assertEqual(AS.getApertureClass("C"), CircleApertureCollector)
        self.assertEqual(AS.getApertureClass("R"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("O"), RectangleApertureCollector)
        self.assertEqual(AS.getApertureClass("P"), PolygonApertureCollector)
        self.assertEqual(AS.getApertureClass(is_region=True), RegionApertureCollector)


if __name__ == "__main__":
    main()
