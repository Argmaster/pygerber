"""`polygon` module contains classes for drawing polygons."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from pygerber.vm.base import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.point import Point

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


class Line(PolygonPart):
    """Draw a line from the current position to the given position."""

    start: Point
    end: Point

    @classmethod
    def from_tuples(cls, start: tuple[float, float], end: tuple[float, float]) -> Self:
        """Create a new line from two tuples."""
        return cls(start=Point.from_tuple(start), end=Point.from_tuple(end))


class Arc(PolygonPart):
    """Draw a arc from the current position to the given position.

    Arcs are always clockwise.
    """

    start: Point
    end: Point

    @classmethod
    def from_tuples(cls, start: tuple[float, float], end: tuple[float, float]) -> Self:
        """Create a new arc from two tuples."""
        return cls(start=Point.from_tuple(start), end=Point.from_tuple(end))
