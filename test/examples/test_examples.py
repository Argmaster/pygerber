from __future__ import annotations

from test.examples import (
    render_copper_from_buffer,
    render_copper_from_buffer_into_buffer,
    render_copper_from_path,
    render_copper_from_path_into_buffer,
    render_copper_from_string,
    render_copper_from_string_into_buffer,
)


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
