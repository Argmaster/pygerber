"""Parser level abstraction of block aperture info for Gerber AST parser, version 2."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.command_buffer2 import (
    ReadonlyCommandBuffer2,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Block2(Aperture2):
    """Parser level abstraction of aperture info for block aperture."""

    command_buffer: ReadonlyCommandBuffer2

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        # Block apertures are resolved into series of commands at parser level.
        raise NotImplementedError

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return self.command_buffer.get_bounding_box()
