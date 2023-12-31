"""Parser level abstraction of draw operation for Gerber AST parser, version 2."""
from __future__ import annotations

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.state_enums import Polarity
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID


class Command2(FrozenGeneralModel):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    attributes: ImmutableMapping = Field(default_factory=ImmutableMapping)
    polarity: Polarity
    aperture_id: ApertureID

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"
