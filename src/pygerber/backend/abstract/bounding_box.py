"""Utility class for calculating bounding boxes of drawing elements."""
from __future__ import annotations

from typing import ClassVar, Tuple

from pydantic import BaseModel, ConfigDict, Field

from pygerber.backend.abstract.offset import Offset


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

    def size(self) -> Size:
        """Get bounding box size."""
        return Size((self.max_x - self.min_x, self.max_y - self.min_y))

    def reposition_to_zero(self) -> BoundingBox:
        """Reposition the bounding box such that its min values are equal to zero."""
        width = self.max_x - self.min_x
        height = self.max_y - self.min_y

        return BoundingBox(
            max_x=width,
            max_y=height,
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


BoundingBox.NULL = BoundingBox(
    max_x=Offset.NULL,
    max_y=Offset.NULL,
    min_x=Offset.NULL,
    min_y=Offset.NULL,
)


class Size(Tuple[Offset, Offset]):
    """Tuple wrapper for representing size with custom accessors."""

    __slots__ = ()

    @property
    def x(self) -> Offset:
        """Return size in X axis."""
        return self[0]

    @property
    def y(self) -> Offset:
        """Return size in X axis."""
        return self[1]

    def as_pixels(self, dpi: int) -> tuple[int, int]:
        """Return size as pixels using given DPI for conversion."""
        return (self.x.as_pixels(dpi), self.y.as_pixels(dpi))
