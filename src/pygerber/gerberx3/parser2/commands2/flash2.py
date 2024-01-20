"""Parser level abstraction of flash operation for Gerber AST parser, version 2."""
from __future__ import annotations

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


class Flash2(ApertureDrawCommand2):
    """Parser level abstraction of flash operation for Gerber AST parser,
    version 2.
    """

    flash_point: Vector2D

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        return self.model_copy(
            update={
                "flash_point": self.flash_point.get_mirrored(mirror),
            },
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        return self.model_copy(
            update={
                "flash_point": self.flash_point + vector,
            },
        )

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        self.aperture.render_flash(renderer, self)

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        return self.aperture.get_bounding_box() + self.flash_point
