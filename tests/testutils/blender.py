# -*- coding: utf-8 -*-
from __future__ import annotations

from types import SimpleNamespace

from pygerber.constants import Polarity
from pygerber.parser.blender.parser import (
    BLENDER_APERTURE_SET,
    DEFAULT_LAYER_GREEN,
    ParserWithBlender,
)
from pygerber.renderer import Renderer


def get_dummy_renderer():
    renderer = Renderer(BLENDER_APERTURE_SET)
    renderer.state.set_polarity(Polarity.DARK)
    ParserWithBlender._inject_layer_spec_to_renderer(
        SimpleNamespace(renderer=renderer, layer_structure=DEFAULT_LAYER_GREEN)
    )
    return renderer
