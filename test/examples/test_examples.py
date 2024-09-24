from __future__ import annotations

from pathlib import Path

import pytest

from pygerber.gerberx3.renderer2.svg import IS_SVG_BACKEND_AVAILABLE
from test.examples import (
    introspect_minimal_example,
    introspect_mixed_inheritance,
    renderer_2_raster_render,
    renderer_2_svg_render,
)

DIRECTORY = Path(__file__).parent


def test_introspect_minimal_example() -> None:
    introspect_minimal_example.main()


def test_introspect_mixed_inheritance() -> None:
    introspect_mixed_inheritance.main()


def test_renderer_2_raster_render() -> None:
    renderer_2_raster_render.render()


@pytest.mark.skipif(not IS_SVG_BACKEND_AVAILABLE, reason="SVG backend required")
def test_renderer_2_svg_render() -> None:
    renderer_2_svg_render.render()
