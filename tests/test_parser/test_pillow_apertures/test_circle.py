# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PIL import Image
from pygerber.constants import Interpolation, Polarity
from pygerber.mathclasses import Vector2D
from pygerber.renderer.spec import ArcSpec, FlashSpec, LineSpec
from tests.testutils.pillow import get_pillow_circle, get_pillow_initialized_renderer


class TestPillowCircle(TestCase):
    def prepare_to_draw(self):
        renderer = get_pillow_initialized_renderer()
        renderer.state.set_polarity(Polarity.DARK)
        return get_pillow_circle(renderer), renderer

    def test_init(self):
        renderer = get_pillow_initialized_renderer()
        self.assertIsNotNone(get_pillow_circle(renderer))

    def test_draw_flash(self):
        circle, renderer = self.prepare_to_draw()
        spec = FlashSpec(Vector2D(0, 0), False)
        circle.flash(spec)
        canvas: Image.Image = renderer.canvas
        # \/ uncomment to see test result
        # circle should be visible
        # canvas.show()

    def test_draw_line(self):
        circle, renderer = self.prepare_to_draw()
        spec = LineSpec(Vector2D(-3, -3), Vector2D(3, 3), False)
        circle.line(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line with rounded edges
        # canvas.show()

    def test_draw_arc_most(self):
        circle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(-3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 70% of circle
        # canvas.show()

    def test_draw_arc_least(self):
        circle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(-3, -2), Vector2D(3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 30% of circle
        # canvas.show()

    def test_draw_arc_half(self):
        circle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.ClockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, 6), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 50% of circle
        # canvas.show()

    def test_draw_arc_half_other(self):
        circle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, 6), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # canvas.show()

    def test_draw_arc_full(self):
        circle, renderer = self.prepare_to_draw()
        renderer.state.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = renderer.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # circle, empty inside
        # canvas.show()


if __name__ == "__main__":
    main()
