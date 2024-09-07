"""`line` module contains Line class, descendant of ShapeSegment class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pyparsing as pp

from pygerber.vm.commands.shape_segments.shape_segment import ShapeSegment
from pygerber.vm.types import Box, Matrix3x3, Vector

if TYPE_CHECKING:
    from typing_extensions import Self


class Line(ShapeSegment):
    """Line segment which can be used to define Shape contents."""

    start: Vector
    end: Vector

    @classmethod
    def from_tuples(cls, start: tuple[float, float], end: tuple[float, float]) -> Self:
        """Create a new line from two tuples."""
        return cls(start=Vector.from_tuple(start), end=Vector.from_tuple(end))

    @pp.cached_property
    def outer_box(self) -> Box:
        """Get outer box of shape segment."""
        return Box.from_vectors(self.start, self.end)

    def transform(self, transform: Matrix3x3) -> Self:
        """Transform points defining this line."""
        return self.__class__(
            start=self.start.transform(transform),
            end=self.end.transform(transform),
        )
