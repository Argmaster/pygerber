# -*- coding: utf-8 -*-
from __future__ import annotations

from unittest import TestCase, main

from PIL import Image
from pygerber.mathclasses import Vector2D
from pygerber.meta.meta import Polarity
from pygerber.meta.spec import ArcSpec, FlashSpec, LineSpec
from pygerber.parser.pillow.apertures.circle import PillowCircle
from tests.testutils.pillow import (
    get_pillow_circle,
    get_pillow_initialized_broker,
    get_pillow_rectangle,
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
        # canvas.show()

    def test_draw_line(self):
        circle, broker = self.prepare_to_draw()
        spec = LineSpec(Vector2D(-3, -3), Vector2D(3, 3), False)
        circle.line(spec)
        canvas: Image.Image = broker.canvas
        # canvas.show()

    def test_draw_arc_most(self):
        circle, broker = self.prepare_to_draw()
        spec = ArcSpec(Vector2D(3, -2), Vector2D(-3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.rotate(180)
        # canvas.show()

    def test_draw_arc_half(self):
        circle, broker = self.prepare_to_draw()
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, 6), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.rotate(180)
        # canvas.show()

    def test_draw_arc_full(self):
        circle, broker = self.prepare_to_draw()
        spec = ArcSpec(Vector2D(3, -2), Vector2D(3, -2), Vector2D(0, 2), False)
        circle.arc(spec)
        canvas: Image.Image = broker.canvas.rotate(180)
        #canvas.show()


class TestPillowRectangle(TestCase):
    def prepare_to_draw(self):
        broker = get_pillow_initialized_broker()
        broker.set_polarity(Polarity.DARK)
        return get_pillow_rectangle(broker), broker

    def test_init(self):
        broker = get_pillow_initialized_broker()
        self.assertIsNotNone(get_pillow_rectangle(broker))

if __name__ == "__main__":
    main()
