"""Module contains exceptions raised by rendering backends."""

from __future__ import annotations


class Renderer2Error(Exception):
    """Base class for exceptions raised by rendering backends."""


class SvgRenderer2Error(Renderer2Error):
    """Error raised by SVG rendering backend."""


class DRAWSVGNotAvailableError(SvgRenderer2Error):
    """Raised when `drawsvg` can't be imported, probably because it was not installed.

    You can install it with `pip install pygerber[svg]`.
    """

    def __init__(self) -> None:
        super().__init__(
            "`drawsvg` library is not available. "
            "Install it with `pip install pygerber[svg]`."
        )
