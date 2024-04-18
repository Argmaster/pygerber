"""Parser level abstraction of obround aperture info for Gerber AST parser,
version 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Obround2(Rectangle2):
    """Parser level abstraction of aperture info for obround aperture."""

    x_size: Offset
    y_size: Offset
    hole_diameter: Optional[Offset]

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        renderer.hooks.render_flash_obround(command, self)
