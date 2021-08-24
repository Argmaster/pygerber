# -*- coding: utf-8 -*-
from pygerber.meta.aperture import RegionApertureManager
from pygerber.meta.meta import Interpolation
from types import SimpleNamespace
from unittest import TestCase, main

from pygerber.exceptions import ApertureSelectionError
from pygerber.meta.broker import DrawingBroker
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.meta.spec import LineSpec
import tests.test_meta.test_aperture as test_aperture


class DrawingBrokerTest(TestCase):
    @staticmethod
    def get_dummy_broker() -> DrawingBroker:
        return DrawingBroker(test_aperture.ApertureSetTest.get_dummy_apertureSet())

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
        except test_aperture.ApertureCollector.CalledWithSpec as e:
            return e.spec
        raise Exception("Failed to catch CalledWithSpec exception.")

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
            test_aperture.ApertureCollector.CalledFlash,
            broker.draw_flash,
            Vector2D(1, 1),
        )
        spec = self.get_collector_spec(broker.draw_flash, Vector2D(1, 1))
        self.assertEqual(spec.location, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_flash_fails_in_regionmode(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        broker.begin_region()
        self.assertRaises(RuntimeError, broker.draw_flash, None)

    def test_draw_line_no_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            test_aperture.ApertureCollector.CalledLine, broker.draw_line, Vector2D(1, 1)
        )
        spec = self.get_collector_spec(broker.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_no_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            test_aperture.ApertureCollector.CalledArc,
            broker.draw_arc,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        spec = self.get_collector_spec(broker.draw_arc, Vector2D(1, 1), Vector2D(0, 2))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.center, Vector2D(0, 2))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_region(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        broker.begin_region()
        self.assertEqual(
            broker.draw_arc(
                Vector2D(1, 1),
                Vector2D(0, 2),
            ),
            None,
        )

    def test_draw_interpolated(self):
        broker = self.get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            test_aperture.ApertureCollector.CalledLine,
            broker.draw_interpolated,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        self.assertRaises(
            test_aperture.ApertureCollector.CalledArc,
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
        self.assertEqual(spec, LineSpec(Vector2D(0, 0), Vector2D(1, 1), True))
        broker.end_region()
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

    def test_fill_xy_none_with_current(self):
        broker = self.get_filled_broker()
        self.assertEqual(
            broker.fill_xy_none_with_current(Vector2D(None, None)), Vector2D(0, 0)
        )

    def test_fill_xy_none_with_zero(self):
        broker = self.get_filled_broker()
        self.assertEqual(
            broker.fill_xy_none_with_zero(Vector2D(None, None)), Vector2D(0, 0)
        )

    def test_bbox_interpolated_line(self):
        broker = self.get_filled_broker()
        broker.set_interpolation(Interpolation.Linear)
        broker.select_aperture(10)
        broker.begin_region()
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_interpolated_arc(self):
        broker = self.get_filled_broker()
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        broker.select_aperture(10)
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, BoundingBox(0.5, 1.5, 1.5, 0.5))
        broker.begin_region()
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_region(self):
        broker = self.get_filled_broker()
        broker.set_interpolation(Interpolation.Linear)
        broker.select_aperture(10)
        broker.begin_region()
        broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        broker.bbox_interpolated(Vector2D(2, 2), Vector2D(0, 1))
        region_aperture, bounds = broker.end_region()
        self.assertEqual(
            region_aperture().bbox(bounds), BoundingBox(0.5, 2.5, 2.5, 0.5)
        )


if __name__ == "__main__":
    main()
