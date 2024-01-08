"""Parser level abstraction of draw line operation for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.state_enums import Mirroring
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

if TYPE_CHECKING:
    from typing_extensions import Self


class Line2(Command2):
    """Parser level abstraction of draw line operation for Gerber AST parser,
    version 2.
    """

    aperture_id: ApertureID
    start_point: Vector2D
    end_point: Vector2D

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        vertex_box = BoundingBox.from_diameter(Offset.new(1))
        return (vertex_box + self.start_point) + (vertex_box + self.end_point)

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        return self.model_copy(
            update={
                "start_point": self.start_point.get_mirrored(mirror),
                "end_point": self.end_point.get_mirrored(mirror),
            },
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        return self.model_copy(
            update={
                "start_point": self.start_point + vector,
                "end_point": self.end_point + vector,
            },
        )
