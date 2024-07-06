"""Utility class for calculating bounding boxes of drawing elements."""

from __future__ import annotations

import operator
from decimal import Decimal
from typing import Callable, ClassVar, Tuple

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D


class BoundingBox(FrozenGeneralModel):
    """Class for calculating bounding boxes."""

    NULL: ClassVar[BoundingBox]

    max_x: Offset = Field(default=Offset.NULL)
    max_y: Offset = Field(default=Offset.NULL)

    min_x: Offset = Field(default=Offset.NULL)
    min_y: Offset = Field(default=Offset.NULL)

    @classmethod
    def from_diameter(cls, diameter: Offset) -> BoundingBox:
        """Create a bounding box from a given diameter."""
        half_diameter = diameter / 2
        return cls(
            max_x=half_diameter,
            max_y=half_diameter,
            min_x=-half_diameter,
            min_y=-half_diameter,
        )

    @classmethod
    def from_rectangle(cls, x_size: Offset, y_size: Offset) -> BoundingBox:
        """Create a bounding box from a given diameter."""
        half_x = x_size / 2
        half_y = y_size / 2
        return cls(
            max_x=half_x,
            max_y=half_y,
            min_x=-half_x,
            min_y=-half_y,
        )

    @property
    def width(self) -> Offset:
        """Return width of the bounding box."""
        return self.max_x - self.min_x

    @property
    def height(self) -> Offset:
        """Return height of the bounding box."""
        return self.max_y - self.min_y

    def get_size(self) -> Vector2D:
        """Get bounding box size."""
        return Vector2D(x=self.width, y=self.height)

    @property
    def center(self) -> Vector2D:
        """Return current center of the bounding box."""
        center_x = (self.max_x + self.min_x) / Offset(value=Decimal(2))
        center_y = (self.max_y + self.min_y) / Offset(value=Decimal(2))
        return Vector2D(x=center_x, y=center_y)

    def get_min_vector(self) -> Vector2D:
        """Return Vector2D of min_x and min_y."""
        return Vector2D(x=self.min_x, y=self.min_y)

    def get_max_vector(self) -> Vector2D:
        """Return Vector2D of min_x and min_y."""
        return Vector2D(x=self.max_x, y=self.max_y)

    def as_pixel_box(
        self,
        dpi: int,
        *,
        dx_max: int = 0,
        dy_max: int = 0,
        dx_min: int = 0,
        dy_min: int = 0,
    ) -> PixelBox:
        """Return box as tuple of ints with order.

        [x0, y0, x1, y1], where x1 >= x0 and y1 >= y0
        """
        return PixelBox(
            (
                self.min_x.as_pixels(dpi) + dx_min,
                self.min_y.as_pixels(dpi) + dy_min,
                self.max_x.as_pixels(dpi) + dx_max,
                self.max_y.as_pixels(dpi) + dy_max,
            ),
        )

    def _operator(
        self,
        other: object,
        op: Callable,
    ) -> BoundingBox:
        if isinstance(other, Vector2D):
            return BoundingBox(
                max_x=op(self.max_x, other.x),
                max_y=op(self.max_y, other.y),
                min_x=op(self.min_x, other.x),
                min_y=op(self.min_y, other.y),
            )
        if isinstance(other, (Offset, Decimal, int, float)):
            return BoundingBox(
                max_x=op(self.max_x, other),
                max_y=op(self.max_y, other),
                min_x=op(self.min_x, -other),
                min_y=op(self.min_y, -other),
            )
        return NotImplemented

    def __add__(self, other: object) -> BoundingBox:
        if isinstance(other, BoundingBox):
            return BoundingBox(
                max_x=max(self.max_x, other.max_x),
                max_y=max(self.max_y, other.max_y),
                min_x=min(self.min_x, other.min_x),
                min_y=min(self.min_y, other.min_y),
            )
        return self._operator(other, operator.add)

    def __sub__(self, other: object) -> BoundingBox:
        return self._operator(other, operator.sub)

    def __mul__(self, other: object) -> BoundingBox:
        return self._operator(other, operator.mul)

    def __truediv__(self, other: object) -> BoundingBox:
        return self._operator(other, operator.truediv)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(max_x={self.max_x}, max_y={self.max_y}, "
            f"min_x={self.min_x}, min_y={self.min_y})"
        )

    def include_point(self, point: Vector2D) -> BoundingBox:
        """Include point in bounding box by extending bounding box overt the point."""
        # Check for the x-coordinate
        new_max_x = max(self.max_x, point.x)
        new_min_x = min(self.min_x, point.x)

        # Check for the y-coordinate
        new_max_y = max(self.max_y, point.y)
        new_min_y = min(self.min_y, point.y)

        return BoundingBox(
            max_x=new_max_x,
            max_y=new_max_y,
            min_x=new_min_x,
            min_y=new_min_y,
        )

    def get_rotated(self, angle: Decimal) -> BoundingBox:
        """Return bounding box rotated around (0, 0)."""
        v_x_max = Vector2D(x=self.max_x, y=Offset.new(0)).get_rotated(-angle)
        v_y_max = Vector2D(x=Offset.new(0), y=self.max_y).get_rotated(-angle)

        v_new_max_0 = v_x_max + v_y_max
        v_new_max_1 = v_x_max - v_y_max

        v_x_min = Vector2D(x=self.min_x, y=Offset.new(0)).get_rotated(-angle)
        v_y_min = Vector2D(x=Offset.new(0), y=self.min_y).get_rotated(-angle)

        v_new_min_0 = v_x_min + v_y_min
        v_new_min_1 = v_x_min - v_y_min

        return BoundingBox(
            max_x=max(v_new_max_0.x, v_new_max_1.x, v_new_min_0.x, v_new_min_1.x),
            max_y=max(v_new_max_0.y, v_new_max_1.y, v_new_min_0.y, v_new_min_1.y),
            min_x=min(v_new_max_0.x, v_new_max_1.x, v_new_min_0.x, v_new_min_1.x),
            min_y=min(v_new_max_0.y, v_new_max_1.y, v_new_min_0.y, v_new_min_1.y),
        )


BoundingBox.NULL = BoundingBox(
    max_x=Offset.NULL,
    max_y=Offset.NULL,
    min_x=Offset.NULL,
    min_y=Offset.NULL,
)


class PixelBox(Tuple[int, int, int, int]):
    """Custom class for representing pixel boxes."""

    __slots__ = ()
