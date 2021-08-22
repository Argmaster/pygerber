# -*- coding: utf-8 -*-
from pygerber.meta.meta import Interpolation
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.exceptions import ApertureSelectionError
from pygerber.meta.broker import DrawingBroker
from pygerber.mathclasses import Vector2D
from pygerber.meta.spec import LineSpec
from tests.test_meta.test_aperture import ApertureSetTest

from .test_aperture import ApertureCollector


class DrawingBrokerTest(TestCase):
    @staticmethod
    def get_dummy_broker() -> DrawingBroker:
        return DrawingBroker(ApertureSetTest.get_dummy_apertureSet())

    @staticmethod
    def fill_dummy_apertures(broker: DrawingBroker):
        broker.define_aperture(
            "C", None, 10, SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0)
        )
        broker.define_aperture(
            "R", None, 11, SimpleNamespace(X=1, Y=1, HOLE_DIAMETER=0)
        )
        broker.define_aperture(
            "P",
            None,
            12,
            SimpleNamespace(DIAMETER=1, VERTICES=6, ROTATION=0, HOLE_DIAMETER=0),
        )
        return broker

    @staticmethod
    def get_filled_broker() -> DrawingBroker:
        return DrawingBrokerTest.fill_dummy_apertures(
            DrawingBrokerTest.get_dummy_broker()
        )

    @staticmethod
    def get_collector_spec(function, *args):
        try:
            function(*args)
        except ApertureCollector.CalledWithSpec as e:
            return e.spec
        raise Exception("Failed to catch CalledWithSpec exception.")

    @staticmethod
    def get_collector_bounds(function, *args):
        try:
            function(*args)
        except ApertureCollector.CalledFinish as e:
            return e.bounds
        raise Exception("Failed to catch CalledFinish exception.")

    def test_select_aperture(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertEqual(broker.current_aperture, broker.apertures[10])

    def test_aperture_not_selected(self):
        broker = self.get_filled_broker()
        self.assertRaises(ApertureSelectionError, broker.draw_flash, Vector2D(1, 1))

    def test_draw_flash_no_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledFlash, broker.draw_flash, Vector2D(1, 1)
        )
        spec = self.get_collector_spec(broker.draw_flash, Vector2D(1, 1))
        self.assertEqual(spec.location, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_draw_line_no_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledLine, broker.draw_line, Vector2D(1, 1)
        )
        spec = self.get_collector_spec(broker.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_no_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledArc,
            broker.draw_arc,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        spec = self.get_collector_spec(broker.draw_arc, Vector2D(1, 1), Vector2D(0, 2))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.center, Vector2D(0, 2))
        self.assertEqual(spec.is_region, False)

    def test_draw_interpolated(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledLine,
            broker.draw_interpolated,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        self.assertRaises(
            ApertureCollector.CalledArc,
            broker.draw_interpolated,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )


    def test_regionmode(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        broker.begin_region()
        broker.draw_line(Vector2D(1, 1))
        self.assertEqual(broker.region_bounds[0][0], broker.current_aperture)
        broker.select_aperture(11)
        self.assertNotEqual(broker.region_bounds[0][0], broker.current_aperture)
        spec: LineSpec = broker.region_bounds[0][1]
        region_bounds = broker.region_bounds
        self.assertEqual(spec, LineSpec(Vector2D(0, 0), Vector2D(1, 1), True))
        bounds = self.get_collector_bounds(broker.end_region)
        self.assertEqual(bounds, region_bounds)
        self.assertEqual(broker.region_bounds, [])
        self.assertFalse(broker.is_regionmode)

    def test_move(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        broker.move_pointer(Vector2D(3, None))
        spec = self.get_collector_spec(broker.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(3, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)


if __name__ == "__main__":
    main()
