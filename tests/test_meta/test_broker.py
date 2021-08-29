# -*- coding: utf-8 -*-
from tests.testutils.apertures import ApertureCollector
from tests.testutils.broker import get_collector_spec, get_filled_broker
from pygerber.meta.meta import Interpolation
from unittest import TestCase, main

from pygerber.exceptions import ApertureSelectionError
from pygerber.mathclasses import BoundingBox, Vector2D
from pygerber.meta.spec import LineSpec


class DrawingBrokerTest(TestCase):

    def test_select_aperture(self):
        broker = get_filled_broker()
        broker.select_aperture(10)
        self.assertEqual(broker.current_aperture, broker.apertures[10])

    def test_aperture_not_selected(self):
        broker = get_filled_broker()
        self.assertRaises(ApertureSelectionError, broker.draw_flash, Vector2D(1, 1))

    def test_draw_flash_no_region(self):
        broker = get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledFlash,
            broker.draw_flash,
            Vector2D(1, 1),
        )
        spec = get_collector_spec(broker.draw_flash, Vector2D(1, 1))
        self.assertEqual(spec.location, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_flash_fails_in_regionmode(self):
        broker = get_filled_broker()
        broker.select_aperture(10)
        broker.begin_region()
        self.assertRaises(RuntimeError, broker.draw_flash, None)

    def test_draw_line_no_region(self):
        broker = get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledLine, broker.draw_line, Vector2D(1, 1)
        )
        spec = get_collector_spec(broker.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_no_region(self):
        broker = get_filled_broker()
        broker.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledArc,
            broker.draw_arc,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        spec = get_collector_spec(broker.draw_arc, Vector2D(1, 1), Vector2D(0, 2))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.center, Vector2D(0, 2))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_region(self):
        broker = get_filled_broker()
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
        broker = get_filled_broker()
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
        broker = get_filled_broker()
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
        broker = get_filled_broker()
        broker.select_aperture(10)
        broker.move_pointer(Vector2D(3, 0))
        spec = get_collector_spec(broker.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(3, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_bbox_interpolated_line(self):
        broker = get_filled_broker()
        broker.set_interpolation(Interpolation.Linear)
        broker.select_aperture(10)
        broker.begin_region()
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_interpolated_arc(self):
        broker = get_filled_broker()
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        broker.select_aperture(10)
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, BoundingBox(-1.5, 2.5, 1.5, -0.5))
        broker.begin_region()
        bbox = broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_region(self):
        broker = get_filled_broker()
        broker.set_interpolation(Interpolation.Linear)
        broker.select_aperture(10)
        broker.begin_region()
        broker.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        broker.bbox_interpolated(Vector2D(2, 2), Vector2D(0, 1))
        region_aperture, bounds = broker.end_region()
        self.assertEqual(
            region_aperture(broker).bbox(bounds), BoundingBox(-0.5, 2.5, 2.5, -0.5)
        )


if __name__ == "__main__":
    main()
