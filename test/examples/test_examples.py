from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from test.examples import (
    introspect_minimal_example,
    introspect_mixed_inheritance,
    render_copper_from_buffer,
    render_copper_from_buffer_into_buffer,
    render_copper_from_path,
    render_copper_from_path_into_buffer,
    render_copper_from_string,
    render_copper_from_string_into_buffer,
    renderer_2_raster_render,
    renderer_2_svg_render,
)
from typing import Generator

import pytest

from pygerber.gerberx3.renderer2.svg import IS_SVG_BACKEND_AVAILABLE

DIRECTORY = Path(__file__).parent


def test_readme_example_1() -> None:
    exec((DIRECTORY / "readme_example_1.py").read_text())  # noqa: S102


def test_readme_example_2() -> None:
    exec((DIRECTORY / "readme_example_2.py").read_text())  # noqa: S102


def test_render_copper_from_buffer() -> None:
    render_copper_from_buffer.render()


def test_render_copper_from_string() -> None:
    render_copper_from_string.render()


def test_render_copper_from_path() -> None:
    render_copper_from_path.render()


def test_render_copper_from_buffer_into_buffer() -> None:
    render_copper_from_buffer_into_buffer.render()


def test_render_copper_from_string_into_buffer() -> None:
    render_copper_from_string_into_buffer.render()


def test_render_copper_from_path_into_buffer() -> None:
    render_copper_from_path_into_buffer.render()


def test_introspect_minimal_example() -> None:
    introspect_minimal_example.main()


def test_introspect_mixed_inheritance() -> None:
    introspect_mixed_inheritance.main()


def test_renderer_2_raster_render() -> None:
    renderer_2_raster_render.render()


@pytest.mark.skipif(not IS_SVG_BACKEND_AVAILABLE, reason="SVG backend required")
def test_renderer_2_svg_render() -> None:
    renderer_2_svg_render.render()


@contextmanager
def cd_to_tempdir() -> Generator[None, None, None]:
    original_cwd = Path.cwd().as_posix()

    with TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        yield
        os.chdir(original_cwd)


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
