"""`polygon` module contains classes for drawing polygons."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from pygerber.vm.base import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.unit import Unit
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self


class PolygonPart(BaseModel):
    """Base class for region parts."""


class Polygon(Command):
    """Draw a line from the current position to the given position."""

    commands: list[PolygonPart]
    negative: bool = False

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit polygon command."""
        visitor.on_polygon(self)

    @classmethod
    def new_rectangle(
        cls, center: tuple[float, float], width: float, height: float, *, negative: bool
    ) -> Self:
        """Create polygon in shape of rectangle."""
        half_height = height / 2
        half_width = width / 2
        return cls(
            commands=[
                Line.from_tuples(
                    (center[0] - half_width, center[1] - half_height),
                    (center[0] + half_width, center[1] - half_height),
                ),
                Line.from_tuples(
                    (center[0] + half_width, center[1] - half_height),
                    (center[0] + half_width, center[1] + half_height),
                ),
                Line.from_tuples(
                    (center[0] + half_width, center[1] + half_height),
                    (center[0] - half_width, center[1] + half_height),
                ),
                Line.from_tuples(
                    (center[0] - half_width, center[1] + half_height),
                    (center[0] - half_width, center[1] - half_height),
                ),
            ],
            negative=negative,
        )

    @classmethod
    def new_circle(
        cls, center: tuple[float, float], diameter: float, *, negative: bool
    ) -> Self:
        """Create polygon in shape of circle."""
        radius = diameter / 2
        return cls(
            commands=[
                Arc.from_tuples(
                    (center[0] - radius, center[1]),
                    (center[0] + radius, center[1]),
                    center=center,
                    clockwise=True,
                ),
                Arc.from_tuples(
                    (center[0] + radius, center[1]),
                    (center[0] - radius, center[1]),
                    center=center,
                    clockwise=True,
                ),
            ],
            negative=negative,
        )


class Line(PolygonPart):
    """Draw a line from the current position to the given position."""

    start: Vector
    end: Vector

    @classmethod
    def from_tuples(cls, start: tuple[float, float], end: tuple[float, float]) -> Self:
        """Create a new line from two tuples."""
        return cls(start=Vector.from_tuple(start), end=Vector.from_tuple(end))


class Arc(PolygonPart):
    """Draw a arc from the current position to the given position.

    Arcs are always clockwise.
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

    def get_radius(self) -> Unit:
        """Get radius of circle arc."""
        return self.get_relative_start_point().length()
