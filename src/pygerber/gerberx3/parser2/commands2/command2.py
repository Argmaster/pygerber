"""Parser level abstraction of draw operation for Gerber AST parser, version 2."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.state2 import ApertureTransform
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Command2(FrozenGeneralModel):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    transform: ApertureTransform

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        raise NotImplementedError

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command."""
        raise NotImplementedError

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        raise NotImplementedError

    def render(self, hooks: Renderer2) -> None:
        """Render draw operation."""
        raise NotImplementedError

    def command_to_json(self) -> str:
        """Dump draw operation."""
        return json.dumps(
            {
                "cls": f"{self.__module__}.{self.__class__.__qualname__}",
                "dict": json.loads(self.model_dump_json()),
            },
        )

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"
