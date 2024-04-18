"""Parser level abstraction of draw line operation for Gerber AST parser, version 2."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.aperture_draw_command2 import (
    ApertureDrawCommand2,
)
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Line2(ApertureDrawCommand2):
    """Parser level abstraction of draw line operation for Gerber AST parser,
    version 2.
    """

    start_point: Vector2D
    end_point: Vector2D

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        vertex_box = self.aperture.get_bounding_box()
        return (vertex_box + self.start_point) + (vertex_box + self.end_point)

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command.

        Mirroring is a NOOP if mirror is `Mirroring.NoMirroring`.
        """
        if mirror == Mirroring.NoMirroring:
            return self
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

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this command rotated around (0, 0)."""
        return self.model_copy(
            update={
                "start_point": self.start_point.get_rotated(angle),
                "end_point": self.end_point.get_rotated(angle),
            },
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        if scale == Decimal("1.0"):
            return self
        return self.model_copy(
            update={
                "start_point": self.start_point.get_scaled(scale),
                "end_point": self.end_point.get_scaled(scale),
                "aperture": self.aperture.get_scaled(scale),
                "transform": self.transform.get_scaled(scale),
            },
        )

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        renderer.hooks.render_line(self)
