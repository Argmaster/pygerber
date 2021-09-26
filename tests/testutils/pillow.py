# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from pygerber.parser.pillow.api import LayerSpec
from PIL import Image, ImageDraw
from pygerber.parser.pillow.parser import ColorSet
from types import SimpleNamespace
from pygerber.parser.pillow.apertures import (
    PillowCircle,
    PillowRectangle,
    PillowObround,
    PillowPolygon,
    PillowCustom,
    PillowRegion,
)
from pygerber.renderer.apertureset import ApertureSet
from pygerber.renderer import Renderer

DEFAULT_TEST_COLOR_SET = ColorSet(
    (120, 120, 255, 255),
    (255, 120, 120, 255),
    (0, 0, 0, 0),
)

DEFAULT_TEST_CANVAS_SIZE = (1600, 1600)


def get_pillow_initialized_renderer(
    size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET
):
    return initialize_parser_attrs(get_pillow_filled_renderer(), size, dpi, colors)


def get_pillow_filled_renderer():
    return Renderer(
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
    renderer, size=DEFAULT_TEST_CANVAS_SIZE, dpi=600, colors=DEFAULT_TEST_COLOR_SET
):
    renderer.colors = colors
    renderer.dpmm = dpi / 25.4
    renderer.canvas = Image.new("RGBA", size, (99, 99, 99, 99))
    renderer.draw_canvas = ImageDraw.Draw(renderer.canvas)
    renderer.canvas_width = renderer.canvas.width
    renderer.canvas_height = renderer.canvas.height
    renderer.left_offset = renderer.canvas.width / 2
    renderer.bottom_offset = renderer.canvas.height / 2
    return renderer


def get_pillow_circle(renderer, diameter=1, hole_diameter=0):
    return PillowCircle(
        SimpleNamespace(DIAMETER=diameter, HOLE_DIAMETER=hole_diameter),
        renderer,
    )


def get_pillow_rectangle(renderer, x=1, y=3, hole_diameter=0):
    return PillowRectangle(
        SimpleNamespace(X=x, Y=y, HOLE_DIAMETER=hole_diameter), renderer
    )


def get_pillow_obround(renderer, x=1, y=3, hole_diameter=0):
    return PillowObround(
        SimpleNamespace(X=x, Y=y, HOLE_DIAMETER=hole_diameter), renderer
    )


def get_pillow_polygon(renderer, diameter=3, vertices=6, rotation=0, hole_diameter=0):
    return PillowPolygon(
        SimpleNamespace(
            DIAMETER=diameter,
            VERTICES=vertices,
            ROTATION=rotation,
            HOLE_DIAMETER=hole_diameter,
        ),
        renderer,
    )


def get_pillow_custom(renderer, **kwargs):
    return PillowCustom(SimpleNamespace(**kwargs), renderer)


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


def get_layerset(GERBER_PATH: Path):
    return [
        LayerSpec(
            GERBER_PATH / "set" / "top_copper.grb",
            ColorSet((40, 143, 40, 255), (60, 181, 60, 255)),
        ),
        LayerSpec(
            GERBER_PATH / "set" / "top_solder_mask.grb",
            ColorSet((153, 153, 153, 255)),
        ),
        LayerSpec(
            GERBER_PATH / "set" / "top_paste_mask.grb",
            ColorSet((117, 117, 117, 255)),
        ),
        LayerSpec(GERBER_PATH / "set" / "top_silk.grb", ColorSet((255, 255, 255, 255))),
    ]
