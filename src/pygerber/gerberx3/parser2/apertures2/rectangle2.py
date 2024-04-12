"""Parser level abstraction of rectangle aperture info for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Rectangle2(Aperture2):
    """Parser level abstraction of aperture info for rectangle aperture."""

    x_size: Offset
    y_size: Offset
    hole_diameter: Optional[Offset]
    rotation: Decimal = Field(default=Decimal("0.0"))

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_rectangle(command, self)

    def get_stroke_width(self) -> Offset:
        """Return stroke width of aperture."""
        return (self.x_size + self.y_size) / 2

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        return BoundingBox.from_rectangle(self.x_size, self.y_size).get_rotated(
            self.rotation,
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        return self.model_copy(
            update={
                "x_size": self.x_size * scale,
                "y_size": self.y_size * scale,
                "hole_diameter": (
                    None if self.hole_diameter is None else self.hole_diameter * scale
                ),
            },
        )

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this aperture rotated around (0, 0)."""
        return self.model_copy(
            update={"rotation": (self.rotation + angle) % Decimal(360)},
        )
