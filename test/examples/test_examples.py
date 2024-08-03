from __future__ import annotations

from pathlib import Path

import pytest

from pygerber.gerberx3.renderer2.svg import IS_SVG_BACKEND_AVAILABLE
from test.conftest import cd_to_tempdir
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


def test_pygerber_api_v2_svg() -> None:
    with cd_to_tempdir():
        exec((DIRECTORY / "pygerber_api_v2_svg.py").read_text())  # noqa: S102
        assert Path("output.svg").exists()


def test_pygerber_api_v2_png() -> None:
    with cd_to_tempdir():
        exec((DIRECTORY / "pygerber_api_v2_png.py").read_text())  # noqa: S102
        assert Path("output.png").exists()


def test_pygerber_api_v2_jpg() -> None:
    with cd_to_tempdir():
        exec((DIRECTORY / "pygerber_api_v2_jpg.py").read_text())  # noqa: S102
        assert Path("output.jpg").exists()


def test_pygerber_api_v2_png_project() -> None:
    with cd_to_tempdir():
        exec((DIRECTORY / "pygerber_api_v2_png_project.py").read_text())  # noqa: S102
        assert Path("output.png").exists()
