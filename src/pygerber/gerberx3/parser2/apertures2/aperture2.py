"""Parser level abstraction of aperture info for Gerber AST parser, version 2."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.attributes2 import ApertureAttributes
from pygerber.gerberx3.state_enums import Mirroring
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

if TYPE_CHECKING:
    from decimal import Decimal

    from typing_extensions import Self

    from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Aperture2(FrozenGeneralModel):
    """Parser level abstraction of aperture info."""

    identifier: ApertureID
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

    def get_mirrored(self, mirror: Mirroring) -> Self:  # noqa: ARG002
        """Get mirrored aperture."""
        return self

    def get_rotated(self, angle: Decimal) -> Self:  # noqa: ARG002
        """Get copy of this aperture rotated around (0, 0)."""
        return self

    def get_scaled(self, scale: Decimal) -> Self:  # noqa: ARG002
        """Get copy of this aperture scaled by factor."""
        return self
