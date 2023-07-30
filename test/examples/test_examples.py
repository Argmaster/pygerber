from test.examples import render_copper_from_buffer, render_copper_from_path
from test.examples import render_copper_from_string


def test_render_copper_from_buffer() -> None:
    render_copper_from_buffer.render()


def test_render_copper_from_string() -> None:
    render_copper_from_string.render()


def test_render_copper_from_path() -> None:
    render_copper_from_path.render()
