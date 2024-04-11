"""Parser level abstraction of draw operation for Gerber AST parser, version 2."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Generator

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.state2 import ApertureTransform
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from decimal import Decimal

    from typing_extensions import Self

    from pygerber.gerberx3.renderer2.abstract import Renderer2


class Command2(FrozenGeneralModel):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    transform: ApertureTransform

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        raise NotImplementedError

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command.

        Mirroring is a NOOP if mirror is `Mirroring.NoMirroring`.
        """
        raise NotImplementedError

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        raise NotImplementedError

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this command rotated around (0, 0)."""
        raise NotImplementedError

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        raise NotImplementedError

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        raise NotImplementedError

    def render_iter(
        self,
        renderer: Renderer2,  # noqa: ARG002
    ) -> Generator[Command2, None, None]:
        """Render draw operation."""
        raise NotImplementedError
        yield  # type: ignore[unreachable]

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
