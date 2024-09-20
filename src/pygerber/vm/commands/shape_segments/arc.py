"""`line` module contains Line class, descendant of ShapeSegment class."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pyparsing as pp

from pygerber.vm.commands.shape_segments.shape_segment import ShapeSegment
from pygerber.vm.types import Matrix3x3, Vector
from pygerber.vm.types.box import Box

if TYPE_CHECKING:
    from typing_extensions import Self


class Arc(ShapeSegment):
    """Arc segment which can be used to define Shape contents.

    Arc resolution is determined at rendering time and dynamically adjusted to provide
    the best image quality. This gives Arc class great advantage over creating arcs
    with multiple manually defined Line segments.
    """

    start: Vector
    end: Vector
    center: Vector
    clockwise: bool

    @classmethod
    def from_tuples(
        cls,
        start: tuple[float, float],
        end: tuple[float, float],
        center: tuple[float, float],
        *,
        clockwise: bool,
    ) -> Self:
        """Create a new arc from two tuples."""
        return cls(
            start=Vector.from_tuple(start),
            end=Vector.from_tuple(end),
            center=Vector.from_tuple(center),
            clockwise=clockwise,
        )

    def get_relative_start_point(self) -> Vector:
        """Get starting point relative to arc center."""
        return self.start - self.center

    def get_relative_end_point(self) -> Vector:
        """Get ending point relative to arc center."""
        return self.end - self.center

    def get_radius(self) -> float:
        """Get radius of circle arc."""
        return self.get_relative_start_point().length()

    def is_valid_arc(self) -> bool:
        """Check if arc is valid."""
        return (
            self.get_relative_start_point().length()
            == self.get_relative_end_point().length()
        )

    @pp.cached_property
    def outer_box(self) -> Box:
        """Get outer box of shape segment."""
        radius = self.get_radius()
        relative_start = self.get_relative_start_point()

        total_angle = relative_start.angle_between(
            self.get_relative_end_point(),
        )

        angle_x_plus = relative_start.angle_between(Vector.unit.x) % 360
        angle_y_minus = relative_start.angle_between(-Vector.unit.y) % 360
        angle_x_minus = relative_start.angle_between(-Vector.unit.x) % 360
        angle_y_plus = relative_start.angle_between(Vector.unit.y) % 360

        vectors = [
            Vector(x=0, y=0),
            relative_start,
            self.get_relative_end_point(),
        ]
        if not self.clockwise:
            total_angle = 360 - total_angle
            angle_x_plus = 360 - angle_x_plus
            angle_y_minus = 360 - angle_y_minus
            angle_x_minus = 360 - angle_x_minus
            angle_y_plus = 360 - angle_y_plus

        if angle_x_plus < total_angle:
            vectors.append(Vector(x=radius, y=0))
        if angle_y_minus < total_angle:
            vectors.append(Vector(x=0, y=-radius))
        if angle_x_minus < total_angle:
            vectors.append(Vector(x=-radius, y=0))
        if angle_y_plus < total_angle:
            vectors.append(Vector(x=0, y=radius))

        return Box.from_vectors(*(v + self.center for v in vectors))

    def transform(self, transform: Matrix3x3) -> Self:
        """Transform points defining this line."""
        return self.__class__(
            start=self.start.transform(transform),
            end=self.end.transform(transform),
            center=self.center.transform(transform),
            clockwise=(
                self.clockwise
                if transform[0][0] * transform[1][1] > 0
                else not self.clockwise
            ),
        )
