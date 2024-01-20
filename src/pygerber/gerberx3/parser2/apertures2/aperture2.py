"""Parser level abstraction of aperture info for Gerber AST parser, version 2."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.attributes2 import ApertureAttributes

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Aperture2(FrozenGeneralModel):
    """Parser level abstraction of aperture info."""

    attributes: ApertureAttributes = Field(default_factory=ImmutableMapping)

    def render_flash(self, renderer: Renderer2, command: Flash2) -> None:
        """Render draw operation."""
        raise NotImplementedError

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of aperture."""
        raise NotImplementedError

    def get_stroke_width(self) -> Offset:
        """Get stroke width of command."""
        raise NotImplementedError
