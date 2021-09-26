# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main

from pygerber.constants import Interpolation
from pygerber.exceptions import ApertureSelectionError
from pygerber.mathclasses import BoundingBox
from pygerber.mathclasses import Vector2D
from pygerber.renderer.spec import LineSpec
from tests.testutils.apertures import ApertureCollector
from tests.testutils.renderer import get_collector_spec
from tests.testutils.renderer import get_filled_renderer


class TestRenderer(TestCase):
    def test_select_aperture(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertEqual(renderer.apertures.current_aperture, renderer.apertures[10])

    def test_aperture_not_selected(self):
        renderer = get_filled_renderer()
        self.assertRaises(ApertureSelectionError, renderer.draw_flash, Vector2D(1, 1))

    def test_draw_flash_no_region(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledFlash,
            renderer.draw_flash,
            Vector2D(1, 1),
        )
        spec = get_collector_spec(renderer.draw_flash, Vector2D(1, 1))
        self.assertEqual(spec.location, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_flash_fails_in_regionmode(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        renderer.state.begin_region()
        self.assertRaises(RuntimeError, renderer.draw_flash, None)

    def test_draw_line_no_region(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledLine, renderer.draw_line, Vector2D(1, 1)
        )
        spec = get_collector_spec(renderer.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_no_region(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledArc,
            renderer.draw_arc,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        spec = get_collector_spec(renderer.draw_arc, Vector2D(1, 1), Vector2D(0, 2))
        self.assertEqual(spec.begin, Vector2D(0, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.center, Vector2D(0, 2))
        self.assertEqual(spec.is_region, False)

    def test_draw_arc_region(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        renderer.state.begin_region()
        self.assertEqual(
            renderer.draw_arc(
                Vector2D(1, 1),
                Vector2D(0, 2),
            ),
            None,
        )

    def test_draw_interpolated(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        self.assertRaises(
            ApertureCollector.CalledLine,
            renderer.draw_interpolated,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )
        renderer.state.set_interpolation(Interpolation.ClockwiseCircular)
        self.assertRaises(
            ApertureCollector.CalledArc,
            renderer.draw_interpolated,
            Vector2D(1, 1),
            Vector2D(0, 2),
        )

    def test_regionmode(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        renderer.state.begin_region()
        renderer.draw_line(Vector2D(1, 1))
        spec: LineSpec = renderer.region_bounds[0]
        self.assertEqual(spec, LineSpec(Vector2D(0, 0), Vector2D(1, 1), True))
        renderer.finish_drawing_region()
        renderer.end_region()
        self.assertEqual(renderer.region_bounds, [])
        self.assertFalse(renderer.state.is_regionmode)

    def test_move(self):
        renderer = get_filled_renderer()
        renderer.select_aperture(10)
        renderer.move_pointer(Vector2D(3, 0))
        spec = get_collector_spec(renderer.draw_line, Vector2D(1, 1))
        self.assertEqual(spec.begin, Vector2D(3, 0))
        self.assertEqual(spec.end, Vector2D(1, 1))
        self.assertEqual(spec.is_region, False)

    def test_bbox_interpolated_line(self):
        renderer = get_filled_renderer()
        renderer.state.set_interpolation(Interpolation.Linear)
        renderer.select_aperture(10)
        renderer.state.begin_region()
        bbox = renderer.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_interpolated_arc(self):
        renderer = get_filled_renderer()
        renderer.state.set_interpolation(Interpolation.ClockwiseCircular)
        renderer.select_aperture(10)
        bbox = renderer.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, BoundingBox(-1.5, 2.5, 1.5, -0.5))
        renderer.state.begin_region()
        bbox = renderer.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        self.assertEqual(bbox, None)

    def test_bbox_region(self):
        renderer = get_filled_renderer()
        renderer.state.set_interpolation(Interpolation.Linear)
        renderer.select_aperture(10)
        renderer.state.begin_region()
        renderer.bbox_interpolated(Vector2D(1, 1), Vector2D(0, 1))
        renderer.bbox_interpolated(Vector2D(2, 2), Vector2D(0, 1))
        region_aperture, bounds = renderer.finish_drawing_region()
        self.assertEqual(region_aperture.bbox(bounds), BoundingBox(0, 2, 1, 2))


if __name__ == "__main__":
    main()
