# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase
from unittest import main

from PIL import Image

from pygerber.constants import Interpolation
from pygerber.constants import Polarity
from pygerber.mathclasses import Vector2D
from pygerber.renderer.spec import ArcSpec
from pygerber.renderer.spec import FlashSpec
from pygerber.renderer.spec import LineSpec
from tests.testutils.pillow import get_pillow_initialized_renderer
from tests.testutils.pillow import get_pillow_rectangle


class TestPillowRectangle(TestCase):
    def prepare_to_draw(self):
        renderer = get_pillow_initialized_renderer()
        renderer.state.set_polarity(Polarity.DARK)
        return get_pillow_rectangle(renderer), renderer

    def test_init(self):
        renderer = get_pillow_initialized_renderer()
        self.assertIsNotNone(get_pillow_rectangle(renderer))

    def test_draw_flash(self):
        rectangle, renderer = self.prepare_to_draw()
        spec = FlashSpec(Vector2D(0, 0), False)
        rectangle.flash(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # rectangle 3:1 in the middle
        # canvas.show()

    def test_draw_line(self):
        rectangle, renderer = self.prepare_to_draw()
        spec = LineSpec(Vector2D(-3, -3), Vector2D(3, 3), False)
        rectangle.line(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line stroked with rectangle
        # canvas.show()

    def test_draw_line_2(self):
        rectangle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = LineSpec(Vector2D(6, -6), Vector2D(3, 3), False)
        rectangle.line(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line stroked with rectangle
        # canvas.show()

    def test_draw_arc_most_ccw(self):
        rectangle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(6, -4), Vector2D(-6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~70% of 'circle'
        # canvas.show()

    def test_draw_arc_least_ccw(self):
        rectangle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(-6, -4), Vector2D(6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~30% of 'circle'
        # canvas.show()

    def test_draw_arc_cw(self):
        rectangle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.ClockwiseCircular)
        spec = ArcSpec(Vector2D(6, -4), Vector2D(-6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~30% of 'circle'
        # canvas.show()


if __name__ == "__main__":
    main()
