# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PIL import Image
from pygerber.mathclasses import Vector2D
from pygerber.meta.meta import Interpolation, Polarity
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from tests.testutils.pillow import (
    get_pillow_circle,
    get_pillow_initialized_broker,
)


class TestPillowCircle(TestCase):
    def prepare_to_draw(self):
        broker = get_pillow_initialized_broker()
        broker.set_polarity(Polarity.DARK)
        return get_pillow_circle(broker), broker

    def test_init(self):
        broker = get_pillow_initialized_broker()
        self.assertIsNotNone(get_pillow_circle(broker))

    def test_draw_flash(self):
        circle, broker = self.prepare_to_draw()
        spec = FlashSpec(Vector2D(0, 0), False)
        circle.flash(spec)
        canvas: Image.Image = broker.canvas
        # \/ uncomment to see test result
        # circle should be visible
        # canvas.show()

    def test_draw_line(self):
        circle, broker = self.prepare_to_draw()
        spec = LineSpec(Vector2D(-3, -3), Vector2D(3, 3), False)
        circle.line(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line with rounded edges
        # canvas.show()

    def test_draw_arc_most(self):
        circle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(-3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 70% of circle
        # canvas.show()

    def test_draw_arc_least(self):
        circle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(-3, -2), Vector2D(3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 30% of circle
        # canvas.show()

    def test_draw_arc_half(self):
        circle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, 6), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc with rounded edges, about 50% of circle
        # canvas.show()

    def test_draw_arc_half_other(self):
        circle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, 6), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # canvas.show()

    def test_draw_arc_full(self):
        circle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # circle, empty inside
        # canvas.show()

if __name__ == "__main__":
    main()