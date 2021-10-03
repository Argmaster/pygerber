# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest import main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to

from pygerber.mathclasses import Vector2D
from pygerber.parser.blender.apertures.circle import BlenderCircle
from pygerber.renderer.spec import FlashSpec, LineSpec
from tests.testutils.blender import get_dummy_renderer

TEMP_LOCAL = Path(__file__).parent / ".temp"
TEMP_LOCAL.mkdir(parents=True, exist_ok=True)


class TestBlenderCircle(TestCase):
    def prepare_to_draw(self):
        wipeScenes()
        return get_dummy_renderer()

    def test_draw_flash(self):
        renderer = self.prepare_to_draw()
        circle = BlenderCircle(SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0), renderer)
        circle.flash(FlashSpec(Vector2D(0, 0), False))
        export_to(TEMP_LOCAL / "circle_flash.blend")

    def test_draw_flash_with_hole(self):
        renderer = self.prepare_to_draw()
        circle = BlenderCircle(SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0.5), renderer)
        circle.flash(FlashSpec(Vector2D(0, 0)))
        export_to(TEMP_LOCAL / "circle_flash_with_hole.blend")

    def test_draw_line(self):
        renderer = self.prepare_to_draw()
        circle = BlenderCircle(SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0), renderer)
        circle.line(LineSpec(Vector2D(0, 0), Vector2D(3, 3)))
        export_to(TEMP_LOCAL / "circle_line.blend")


if __name__ == "__main__":
    main()
