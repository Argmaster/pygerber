"""Parser level abstraction of flash operation for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.state_enums import Mirroring
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

if TYPE_CHECKING:
    from typing_extensions import Self


class Flash2(Command2):
    """Parser level abstraction of flash operation for Gerber AST parser,
    version 2.
    """

    aperture_id: ApertureID
    flash_point: Vector2D

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        return self.model_copy(
            update={
                "flash_point": self.flash_point.get_mirrored(mirror),
            },
        )
