"""`polygon` module contains classes for drawing polygons."""

from __future__ import annotations

from pydantic import BaseModel

from pygerber.vm.base import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.point import Point


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


class Arc(PolygonPart):
    """Draw a arc from the current position to the given position.

    Arcs are always clockwise.
    """

    start: Point
    end: Point
