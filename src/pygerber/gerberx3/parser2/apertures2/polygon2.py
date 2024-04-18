"""Parser level abstraction of polygon aperture info for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from decimal import Decimal  # noqa: TCH003
from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Polygon2(Aperture2):
    """Parser level abstraction of aperture info for polygon aperture."""

    outer_diameter: Offset
    number_vertices: int
    rotation: Decimal
    hole_diameter: Optional[Offset]

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_polygon(command, self)

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return BoundingBox.from_diameter(self.outer_diameter)

    def get_stroke_width(self) -> Offset:
        """Get stroke width of command."""
        return self.outer_diameter

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        return self.model_copy(
            update={
                "outer_diameter": self.outer_diameter * scale,
                "hole_diameter": (
                    None if self.hole_diameter is None else self.hole_diameter * scale
                ),
            },
        )
