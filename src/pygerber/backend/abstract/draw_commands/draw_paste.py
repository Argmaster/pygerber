"""Base class for creating components for aperture creation."""

from __future__ import annotations

from functools import cached_property

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawPaste(DrawCommand):
    """Description of aperture component."""

    other: DrawingTarget
    center_position: Vector2D

    def __init__(
        self,
        backend: Backend,
        polarity: Polarity,
        other: DrawingTarget,
        center_position: Vector2D,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.other = other
        self.center_position = center_position

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        return self.other.bounding_box + self.center_position
