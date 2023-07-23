"""Utility class for calculating bounding boxes of drawing elements."""
from __future__ import annotations

from decimal import Decimal
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from pygerber.backend.abstract.offset import Offset
from pygerber.backend.abstract.vector_2d import Vector2D


class BoundingBox(BaseModel):
    """Class for calculating bounding boxes."""

    model_config = ConfigDict(frozen=True)
    NULL: ClassVar[BoundingBox]

    max_x: Offset = Field(default=Offset.NULL)
    max_y: Offset = Field(default=Offset.NULL)

    min_x: Offset = Field(default=Offset.NULL)
    min_y: Offset = Field(default=Offset.NULL)

    @classmethod
    def from_diameter(cls, diameter: Offset) -> BoundingBox:
        """Create a bounding box from a given diameter."""
        half_diameter = diameter.value / 2
        return cls(
            max_x=Offset(value=half_diameter),
            max_y=Offset(value=half_diameter),
            min_x=Offset(value=-half_diameter),
            min_y=Offset(value=-half_diameter),
        )

    def __add__(self, other: object) -> BoundingBox:
        """Add two bounding boxes."""
        if not isinstance(other, BoundingBox):
            msg = "BoundingBox can only be added to another bounding box."
            raise TypeError(msg)

        return BoundingBox(
            max_x=max(self.max_x, other.max_x),
            max_y=max(self.max_y, other.max_y),
            min_x=min(self.min_x, other.min_x),
            min_y=min(self.min_y, other.min_y),
        )

    @property
    def width(self) -> Offset:
        """Return width of the bounding box."""
        return self.max_x - self.min_x

    @property
    def height(self) -> Offset:
        """Return height of the bounding box."""
        return self.max_y - self.min_y

    def size(self) -> Vector2D:
        """Get bounding box size."""
        return Vector2D(x=self.width, y=self.height)

    @property
    def center(self) -> Vector2D:
        """Return current center of the bounding box."""
        center_x = (self.max_x + self.min_x) / Offset(value=Decimal(2))
        center_y = (self.max_y + self.min_y) / Offset(value=Decimal(2))
        return Vector2D(x=center_x, y=center_y)

    def reposition_to_zero(self) -> BoundingBox:
        """Reposition the bounding box such that its min values are equal to zero."""
        return BoundingBox(
            max_x=self.width,
            max_y=self.height,
            min_x=Offset.NULL,
            min_y=Offset.NULL,
        )

    def as_pixel_box(
        self,
        dpi: int,
        *,
        min_value_correction: int = 0,
        max_value_correction: int = 0,
    ) -> tuple[int, int, int, int]:
        """Return box as tuple of ints with order.

        [x0, y0, x1, y1], where x1 >= x0 and y1 >= y0
        """
        return (
            self.min_x.as_pixels(dpi) + min_value_correction,
            self.min_y.as_pixels(dpi) + min_value_correction,
            self.max_x.as_pixels(dpi) + max_value_correction,
            self.max_y.as_pixels(dpi) + max_value_correction,
        )

    def center_at(self, position: Vector2D) -> BoundingBox:
        """Return bounding box with same size centered at given position."""
        dx = position.x - self.center.x
        dy = position.y - self.center.y

        return BoundingBox(
            max_x=self.max_x + dx,
            max_y=self.max_y + dy,
            min_x=self.min_x + dx,
            min_y=self.min_y + dy,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(max_x={self.max_x}, max_y={self.max_y}, "
            f"min_x={self.min_x}, min_y={self.min_y})"
        )


BoundingBox.NULL = BoundingBox(
    max_x=Offset.NULL,
    max_y=Offset.NULL,
    min_x=Offset.NULL,
    min_y=Offset.NULL,
)
