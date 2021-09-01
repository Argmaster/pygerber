# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PIL import Image
from pygerber.mathclasses import Vector2D
from pygerber.meta.meta import Interpolation, Polarity
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from tests.testutils.pillow import (
    get_pillow_initialized_broker,
    get_pillow_obround,
)


class TestPillowObround(TestCase):
    def prepare_to_draw(self):
        broker = get_pillow_initialized_broker()
        broker.set_polarity(Polarity.DARK)
        return get_pillow_obround(broker), broker

    def test_init(self):
        broker = get_pillow_initialized_broker()
        self.assertIsNotNone(get_pillow_obround(broker))

    def test_draw_flash(self):
        rectangle, broker = self.prepare_to_draw()
        spec = FlashSpec(Vector2D(0, 0), False)
        rectangle.flash(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # rectangle 3:1 in the middle
        # canvas.show()

    def test_draw_line(self):
        rectangle, broker = self.prepare_to_draw()
        spec = LineSpec(Vector2D(-3, -3), Vector2D(3, 3), False)
        rectangle.line(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line stroked with rectangle
        # canvas.show()

    def test_draw_line_2(self):
        rectangle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = LineSpec(Vector2D(6, -6), Vector2D(3, 3), False)
        rectangle.line(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # line stroked with rectangle
        # canvas.show()

    def test_draw_arc_most_ccw(self):
        rectangle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(6, -4), Vector2D(-6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~70% of 'circle'
        # canvas.show()

    def test_draw_arc_least_ccw(self):
        rectangle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.CounterclockwiseCircular)
        spec = ArcSpec(Vector2D(-6, -4), Vector2D(6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~30% of 'circle'
        # canvas.show()

    def test_draw_arc_cw(self):
        rectangle, broker = self.prepare_to_draw()
        broker.set_interpolation(Interpolation.ClockwiseCircular)
        spec = ArcSpec(Vector2D(6, -4), Vector2D(-6, -4), Vector2D(0, 4), False)
        rectangle.arc(spec)
        canvas: Image.Image = broker.canvas.transpose(Image.FLIP_TOP_BOTTOM)
        # arc stroked with rectangle, ~30% of 'circle'
        # canvas.show()


if __name__ == "__main__":
    main()
