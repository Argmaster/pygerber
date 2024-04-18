"""# DrawVectorLine Module.

This module defines the base class for creating vector line components
used in drawing creation. The main class, `DrawVectorLine`, represents
a vector line defined by its start and end positions and width.
"""

from __future__ import annotations

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.state_enums import Polarity


class DrawVectorLine(DrawCommand):
    """Represents a vector line component used in drawing creation.
    This class is defined by its start position, end position, and width.
    """

    start_position: Vector2D
    end_position: Vector2D
    width: Offset

    def __init__(
        self,
        backend: Backend,
        polarity: Polarity,
        start_position: Vector2D,
        end_position: Vector2D,
        width: Offset,
    ) -> None:
        """Initialize draw command."""
        super().__init__(backend, polarity)
        self.start_position = start_position
        self.end_position = end_position
        self.width = width

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        vertex_box = BoundingBox.from_diameter(self.width)
        return (vertex_box + self.start_position) + (vertex_box + self.end_position)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}({self.polarity}) start: "
            "{self.start_position} end: {self.end_position}"
        )
