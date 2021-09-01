# -*- coding: utf-8 -*-
from __future__ import annotations
from PIL import Image, ImageDraw
from pygerber.parser.pillow.parser import ColorSet
from types import SimpleNamespace
from pygerber.parser.pillow.apertures import *
from pygerber.meta.apertureset import ApertureSet
from pygerber.meta.broker import DrawingBroker

DEFAULT_TEST_COLOR_SET = ColorSet(
    (120, 120, 255, 255),
    (255, 120, 120, 255),
    (0, 0, 0, 0),
)

DEFAULT_TEST_CANVAS_SIZE = (1600, 1600)


def get_pillow_initialized_broker(
    size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET
):
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


def initialize_parser_attrs(
    broker, size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET
):
    broker.colors = colors
    broker.dpmm = dpi / 25.4
    broker.canvas = Image.new("RGBA", size, (99, 99, 99, 99))
    broker.draw_canvas = ImageDraw.Draw(broker.canvas)
    broker.canvas_width = broker.canvas.width
    broker.canvas_height = broker.canvas.height
    broker.left_offset = broker.canvas.width / 2
    broker.bottom_offset = broker.canvas.height / 2
    return broker


def get_pillow_circle(broker, diameter=1, hole_diameter=0):
    return PillowCircle(
        SimpleNamespace(DIAMETER=diameter, HOLE_DIAMETER=hole_diameter),
        broker,
    )


def get_pillow_rectangle(broker, x=1, y=3, hole_diameter=0):
    return PillowRectangle(
        SimpleNamespace(X=x, Y=y, HOLE_DIAMETER=hole_diameter), broker
    )


def get_pillow_obround(broker, x=1, y=3, hole_diameter=0):
    return PillowObround(SimpleNamespace(X=x, Y=y, HOLE_DIAMETER=hole_diameter), broker)


def get_pillow_polygon(broker, diameter=3, vertices=6, rotation=0, hole_diameter=0):
    return PillowPolygon(
        SimpleNamespace(
            DIAMETER=diameter,
            VERTICES=vertices,
            ROTATION=rotation,
            HOLE_DIAMETER=hole_diameter,
        ),
        broker,
    )


def get_pillow_custom(broker, **kwargs):
    return PillowCustom(SimpleNamespace(**kwargs), broker)


def are_images_similar(
    img1: Image.Image,
    img2: Image.Image,
    color_tolerance: float = 0,
    content_tolerance: float = 0,
):
    if img1.size != img2.size:
        return False
    misses = 0
    for x in range(img1.width):
        for y in range(img2.height):
            r, g, b, a = img1.getpixel((x, y))
            R, G, B, A = img2.getpixel((x, y))
            if not compare_color(r, R, color_tolerance):
                misses += 1
            if not compare_color(g, G, color_tolerance):
                misses += 1
            if not compare_color(b, B, color_tolerance):
                misses += 1
            if not compare_color(a, A, color_tolerance):
                misses += 1
    if misses / (img1.width * img1.height) <= content_tolerance:
        return True
    else:
        return False


def compare_color(c: float, C: float, tresh: float):
    c = c / 255
    C = C / 255
    cC = abs(c - C)
    return cC <= tresh
