"""Contains class wrapping list of draw operations created by Gerber parser."""

from __future__ import annotations

from pygerber.backend.abstract.draw_commands_handle import DrawCommandsHandle


class Rasterized2DDrawActionsHandle(DrawCommandsHandle):
    """List of drawing operations produced by Gerber parser."""
