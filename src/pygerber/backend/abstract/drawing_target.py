"""Target for Draw commands to draw into."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar

from pygerber.backend.abstract.bounding_box import BoundingBox
from pygerber.backend.abstract.vector_2d import Vector2D

if TYPE_CHECKING:
    from types import TracebackType

ExcType = TypeVar("ExcType", bound=BaseException)


class DrawingTarget:
    """Target for Draw commands to draw into."""

    coordinate_origin: Vector2D
    bounding_box: BoundingBox

    def __init__(self, coordinate_origin: Vector2D, bounding_box: BoundingBox) -> None:
        """Initialize drawing target."""
        self.coordinate_origin = coordinate_origin
        self.bounding_box = bounding_box

    def __enter__(self) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[type[ExcType]],
        exc_value: Optional[ExcType],
        traceback: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            self._finalize()

    def _finalize(self) -> None:
        """Call at the end of image modification.

        After this call no modifications to image are allowed.
        """
