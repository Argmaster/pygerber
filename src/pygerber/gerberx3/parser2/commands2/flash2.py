"""Parser level abstraction of flash operation for Gerber AST parser, version 2."""

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


class Flash2(ApertureDrawCommand2):
    """Parser level abstraction of flash operation for Gerber AST parser,
    version 2.
    """

    flash_point: Vector2D

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command.

        Mirroring is a NOOP if mirror is `Mirroring.NoMirroring`.
        """
        if mirror == Mirroring.NoMirroring:
            return self
        return self.model_copy(
            update={
                "flash_point": self.flash_point.get_mirrored(mirror),
                "aperture": self.aperture.get_mirrored(mirror),
            },
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        return self.model_copy(
            update={
                "flash_point": self.flash_point + vector,
            },
        )

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this command rotated around (0, 0)."""
        return self.model_copy(
            update={
                "flash_point": self.flash_point.get_rotated(angle),
                "aperture": self.aperture.get_rotated(angle),
            },
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        if scale == Decimal("1.0"):
            return self
        return self.model_copy(
            update={
                "flash_point": self.flash_point.get_scaled(scale),
                "aperture": self.aperture.get_scaled(scale),
                "transform": self.transform.get_scaled(scale),
            },
        )

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        self.aperture.render_flash(renderer, self)

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        return self.aperture.get_bounding_box() + self.flash_point
