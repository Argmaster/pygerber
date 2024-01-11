"""Parser level abstraction of aperture info for Gerber AST parser, version 2."""
from __future__ import annotations

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.parser2.attributes2 import ApertureAttributes


class Aperture2(FrozenGeneralModel):
    """Parser level abstraction of aperture info."""

    attributes: ApertureAttributes = Field(default_factory=ImmutableMapping)

    def get_bounding_box_size(self) -> BoundingBox:
        """Return bounding box of aperture."""
        raise NotImplementedError
