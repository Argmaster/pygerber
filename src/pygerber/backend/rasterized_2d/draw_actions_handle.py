"""Contains class wrapping list of draw operations created by Gerber parser."""
from __future__ import annotations

from pygerber.backend.abstract.draw_actions_handle import DrawActionsHandle


class Rasterized2DDrawActionsHandle(DrawActionsHandle):
    """List of drawing operations produced by Gerber parser."""
