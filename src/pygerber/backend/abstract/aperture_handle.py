"""Module contains classes-handles to drawing apertures."""

from __future__ import annotations

from abc import abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from pygerber.backend.abstract.backend_cls import Backend
from pygerber.backend.abstract.draw_commands.draw_circle import (
    DrawCircle,
)
from pygerber.backend.abstract.drawing_target import DrawingTarget
from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID

if TYPE_CHECKING:
    from pathlib import Path
    from types import TracebackType

    from pygerber.backend.abstract.draw_commands.draw_command import DrawCommand


class PrivateApertureHandle:
    """Base class for creating Gerber X3 apertures."""

    drawing_target: DrawingTarget
    bounding_box: BoundingBox

    def __init__(
        self,
        aperture_id: ApertureID,
        private_id: int,
        backend: Backend,
    ) -> None:
        """Initialize aperture handle."""
        self.aperture_id = aperture_id
        self.private_id = private_id
        self.backend = backend
        self.aperture_draws: list[DrawCommand] = []
        self.is_plain_circle = True

    def add_draw(self, draw: DrawCommand) -> None:
        """Add circle to aperture."""
        if self.is_plain_circle and (
            not isinstance(draw, DrawCircle) or len(self.aperture_draws) > 1
        ):
            self.is_plain_circle = False
        self.aperture_draws.append(draw)

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            self.bounding_box = self.get_bounding_box()
            self.coordinate_origin = self._get_coordinate_origin()
            self.drawing_target = self._create_drawing_target()

    def finalize_aperture_creation(self) -> None:
        """Draw aperture and store result."""
        with self.drawing_target:
            for aperture_draw in self.aperture_draws:
                aperture_draw.draw(self.drawing_target)

        self._post_drawing_hook()

    def get_bounding_box(self) -> BoundingBox:
        """Return bounding box of draw operation."""
        return self._bounding_box

    @cached_property
    def _bounding_box(self) -> BoundingBox:
        bbox: Optional[BoundingBox] = None

        for aperture_draw in self.aperture_draws:
            if bbox is not None:
                bbox += aperture_draw.get_bounding_box()
            else:
                bbox = aperture_draw.get_bounding_box()

        if bbox is not None:
            return bbox

        return BoundingBox.NULL

    def _get_coordinate_origin(self) -> Vector2D:
        return self.bounding_box.get_min_vector()

    @abstractmethod
    def _create_drawing_target(self) -> DrawingTarget:
        """Create drawing target object."""

    def _post_drawing_hook(self) -> None:
        """Perform custom actions after drawing."""

    def get_public_handle(self) -> PublicApertureHandle:
        """Return immutable aperture handle."""
        return PublicApertureHandle(
            aperture_id=self.aperture_id,
            private_id=self.private_id,
        )

    def get_line_width(self) -> Offset:
        """Width of line made with this aperture."""
        box = self.get_bounding_box()
        return (box.height + box.width) / 2

    @abstractmethod
    def dump_aperture(self, dest: Path) -> None:
        """Save aperture to local file, mainly for debugging purposes."""

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(aperture_id={self.aperture_id}, "
            f"private_id={self.private_id})"
        )

    __repr__ = __str__


class PublicApertureHandle(FrozenGeneralModel):
    """Immutable handle to drawing aperture."""

    aperture_id: ApertureID
    private_id: int
