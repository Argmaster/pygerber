"""Parser level abstraction of rectangle aperture info for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Rectangle2(Aperture2):
    """Parser level abstraction of aperture info for rectangle aperture."""

    x_size: Offset
    y_size: Offset
    hole_diameter: Optional[Offset]

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_rectangle(command, self)

    def get_stroke_width(self) -> Offset:
        """Return stroke width of aperture."""
        return (self.x_size + self.y_size) / 2

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return BoundingBox.from_rectangle(self.x_size, self.y_size)
