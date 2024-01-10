"""Parser level abstraction of flash operation for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.aperture_draw_command2 import (
    ApertureDrawCommand2,
)
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self


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
