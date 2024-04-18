"""Contains class wrapping list of draw operations created by Gerber parser."""

from __future__ import annotations

from typing import List

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.result_handle import ResultHandle


class DrawCommandsHandle:
    """List of drawing operations produced by Gerber parser."""

    def __init__(self, draw_actions: List[DrawCommand], backend: Backend) -> None:
        """Initialize drawing instructions."""
        self.draw_commands = draw_actions
        self.backend = backend

    def draw(self) -> ResultHandle:
        """Create visualization based on drawing instructions."""
        return self.backend.draw(self.draw_commands)
