"""Parser level abstraction of macro aperture info for Gerber AST parser, version 2."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Macro2(Aperture2):
    """Parser level abstraction of aperture info for macro aperture."""

    command_buffer: ReadonlyCommandBuffer2

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_macro(command, self)

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return self.command_buffer.get_bounding_box()

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored aperture."""
        if mirror == Mirroring.NoMirroring:
            return self
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_mirrored(mirror),
            },
        )

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this aperture rotated around (0, 0)."""
        if angle == Decimal("0.0"):
            return self
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_rotated(angle),
            },
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        if scale == Decimal("1.0"):
            return self
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_scaled(scale),
            },
        )
