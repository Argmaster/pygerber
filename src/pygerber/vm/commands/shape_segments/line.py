"""`line` module contains Line class, descendant of ShapeSegment class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pyparsing as pp

from pygerber.vm.commands.shape_segments.shape_segment import ShapeSegment
from pygerber.vm.types.box import AutoBox
from pygerber.vm.types.vector import Vector

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
    def outer_box(self) -> AutoBox:
        """Get outer box of shape segment."""
        return AutoBox.from_vectors(self.start, self.end)
