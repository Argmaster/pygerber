# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest import main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to

from pygerber.mathclasses import Vector2D
from pygerber.parser.blender.apertures.rectangle import BlenderRectangle
from pygerber.renderer.spec import FlashSpec
from tests.testutils.blender import get_dummy_renderer

TEMP_LOCAL = Path(__file__).parent / ".temp"
TEMP_LOCAL.mkdir(parents=True, exist_ok=True)


class TestBlenderRectangle(TestCase):
    def prepare_to_draw(self):
        wipeScenes()
        return get_dummy_renderer()

    def test_draw_flash(self):
        renderer = self.prepare_to_draw()
        circle = BlenderRectangle(
            SimpleNamespace(X=1.0, Y=2.0, HOLE_DIAMETER=0), renderer
        )
        circle.flash(FlashSpec(Vector2D(0.0, 0.0), False))
        export_to(TEMP_LOCAL / "rectangle_flash.blend")

    def test_draw_flash_with_hole(self):
        renderer = self.prepare_to_draw()
        circle = BlenderRectangle(
            SimpleNamespace(X=1, Y=2, HOLE_DIAMETER=0.4), renderer
        )
        circle.flash(FlashSpec(Vector2D(0.0, 0.0), False))
        export_to(TEMP_LOCAL / "rectangle_flash_with_hole.blend")


if __name__ == "__main__":
    main()
