"""Rectangle component for creating apertures."""
from __future__ import annotations

from functools import cached_property

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawRectangle(DrawCommand):
    """Description of rectangle aperture component."""

    center_position: Vector2D
    x_size: Offset
    y_size: Offset

    def __init__(  # noqa: PLR0913
        self,
        backend: Backend,
        polarity: Polarity,
        center_position: Vector2D,
        x_size: Offset,
        y_size: Offset,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.center_position = center_position
        self.x_size = x_size
        self.y_size = y_size

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        return (
            BoundingBox.from_rectangle(self.x_size, self.y_size) + self.center_position
        )
