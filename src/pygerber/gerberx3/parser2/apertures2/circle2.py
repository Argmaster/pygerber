"""Parser level abstraction of circle aperture info for Gerber AST parser, version 2."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Circle2(Aperture2):
    """Parser level abstraction of aperture info for circle aperture."""

    diameter: Offset
    hole_diameter: Optional[Offset]

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_circle(command, self)

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        return BoundingBox.from_diameter(self.diameter)

    def get_stroke_width(self) -> Offset:
        """Get stroke width of command."""
        return self.diameter

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        if scale == Decimal("1.0"):
            return self
        return self.model_copy(
            update={
                "diameter": (self.diameter * scale),
                "hole_diameter": (
                    None if self.hole_diameter is None else self.hole_diameter * scale
                ),
            },
        )


class NoCircle2(Circle2):
    """Dummy aperture representing case when aperture is not needed but has to be
    given to denote width of draw line command.
    """

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_no_circle(command, self)
