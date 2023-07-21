"""Contains class wrapping list of draw operations created by Gerber parser."""
from __future__ import annotations

from typing import List

from pygerber.backend.abstract.draw_actions.draw_action import DrawAction


class DrawList(List[DrawAction]):
    """List of drawing operations produced by Gerber parser."""
