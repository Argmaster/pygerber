# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest import main

from PyR3.shortcut.context import wipeScenes
from PyR3.shortcut.io import export_to

from pygerber.constants import Polarity
from pygerber.mathclasses import Vector2D
from pygerber.parser.blender.apertures.circle import BlenderCircle
from pygerber.parser.blender.parser import BLENDER_APERTURE_SET
from pygerber.parser.blender.parser import DEFAULT_LAYER_GREEN
from pygerber.parser.blender.parser import ParserWithBlender
from pygerber.renderer import Renderer
from pygerber.renderer.spec import FlashSpec

TEMP_LOCAL = Path(__file__).parent / ".temp"
TEMP_LOCAL.mkdir(parents=True, exist_ok=True)


class TestBlenderCircle(TestCase):
    def prepare_to_draw(self):
        wipeScenes()
        renderer = Renderer(BLENDER_APERTURE_SET)
        renderer.state.set_polarity(Polarity.DARK)
        ParserWithBlender._inject_layer_spec_to_renderer(
            SimpleNamespace(renderer=renderer, layer_spec=DEFAULT_LAYER_GREEN)
        )
        return renderer

    def test_draw_flash(self):
        renderer = self.prepare_to_draw()
        circle = BlenderCircle(SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0), renderer)
        circle.flash(FlashSpec(Vector2D(0, 0), False))
        export_to(TEMP_LOCAL / "circle_flash.blend")

    def test_draw_flash_with_hole(self):
        renderer = self.prepare_to_draw()
        circle = BlenderCircle(SimpleNamespace(DIAMETER=1, HOLE_DIAMETER=0.5), renderer)
        circle.flash(FlashSpec(Vector2D(0, 0), False))
        export_to(TEMP_LOCAL / "circle_flash_with_hole.blend")


if __name__ == "__main__":
    main()
