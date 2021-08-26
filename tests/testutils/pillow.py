# -*- coding: utf-8 -*-
from __future__ import annotations
from PIL import Image, ImageDraw
from pygerber.parser.pillow.parser import DEFAULT_COLOR_SET, ColorSet
from types import SimpleNamespace
from pygerber.parser.pillow.apertures import *
from pygerber.meta.apertureset import ApertureSet
from pygerber.meta.broker import DrawingBroker

DEFAULT_TEST_COLOR_SET = ColorSet(
    (120,120,255,255),
    (255,120,120,255),
    (120,255,120,255),
)

DEFAULT_TEST_CANVAS_SIZE = (1600, 1600)

def get_pillow_initialized_broker(size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET):
    return initialize_parser_attrs(get_pillow_filled_broker(), size, dpi, colors)


def get_pillow_filled_broker():
    return DrawingBroker(
        ApertureSet(
            PillowCircle,
            PillowRectangle,
            PillowObround,
            PillowPolygon,
            PillowCustom,
            PillowRegion,
        )
    )


def initialize_parser_attrs(broker, size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET):
    broker.colors = colors
    broker.dpmm = dpi / 25.4
    broker.canvas = Image.new("RGBA", size, (99, 99, 99, 99))
    broker.draw_canvas = ImageDraw.Draw(broker.canvas)
    broker.canvas_width = broker.canvas.width
    broker.canvas_height = broker.canvas.height
    broker.canvas_width_half = broker.canvas.width / 2
    broker.canvas_height_half = broker.canvas.height / 2
    return broker


def get_pillow_circle(broker, diameter=1, hole_diameter=0):
    return PillowCircle(
        SimpleNamespace(DIAMETER=diameter, HOLE_DIAMETER=hole_diameter),
        broker,
    )

def get_pillow_rectangle(broker, x=1, y=3, hole_diameter=0):
    return PillowRectangle(
        SimpleNamespace(X=x, Y=y, HOLE_DIAMETER=hole_diameter),
        broker
    )