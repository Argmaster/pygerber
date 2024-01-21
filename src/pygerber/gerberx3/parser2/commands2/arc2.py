"""Parser level abstraction of draw arc operation for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.aperture_draw_command2 import (
    ApertureDrawCommand2,
)
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Arc2(ApertureDrawCommand2):
    """Parser level abstraction of draw arc operation for Gerber AST parser,
    version 2.
    """

    start_point: Vector2D
    end_point: Vector2D
    center_point: Vector2D

    def get_relative_start_point(self) -> Vector2D:
        """Get starting point relative to arc center."""
        return self.start_point - self.center_point

    def get_relative_end_point(self) -> Vector2D:
        """Get ending point relative to arc center."""
        return self.end_point - self.center_point

    def get_relative_center_point(self) -> Vector2D:
        """Get center point relative to arc center."""
        return self.center_point - self.center_point

    def get_radius(self) -> Offset:
        """Get radius of circle arc."""
        return self.get_relative_start_point().length()

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of arc."""
        return (
            BoundingBox.from_diameter(
                (self.get_radius() * 2) + (self.aperture.get_stroke_width() * 2),
            )
            + self.center_point
        )

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        return self.model_copy(
            update={
                "start_point": self.start_point.get_mirrored(mirror),
                "end_point": self.end_point.get_mirrored(mirror),
                "center_point": self.center_point.get_mirrored(mirror),
            },
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        return self.model_copy(
            update={
                "start_point": self.start_point + vector,
                "end_point": self.end_point + vector,
                "center_point": self.center_point + vector,
            },
        )

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        renderer.hooks.render_arc(self)


class CCArc2(Arc2):
    """Parser level abstraction of draw counterclockwise arc operation for Gerber AST
    parser, version 2.
    """

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        renderer.hooks.render_cc_arc(self)
