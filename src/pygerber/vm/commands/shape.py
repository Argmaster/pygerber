"""`shape` module contains classes for drawing shapes consisting of connected lines
and arcs filled with solid color.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import pyparsing as pp
from pydantic import Field

from pygerber.vm.commands.command import Command
from pygerber.vm.commands.shape_segments import Arc, Line, ShapeSegment
from pygerber.vm.types.box import AutoBox
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.vm.vm import CommandVisitor


class Shape(Command):
    """`Shape` command instructs VM to render a shape described by series of
    lines and arcs into currently active layer.

    Last point of first segment (line or arc) is always connected to the first point
    first segment, so shapes are implicitly closed. If those points are not overlapping,
    they are connected by a straight line.
    """

    commands: List[ShapeSegment] = Field(min_length=1)
    negative: bool = False

    @pp.cached_property
    def outer_box(self) -> AutoBox:
        """Get outer box of shape segment."""
        accumulator = self.commands[0].outer_box
        for segment in self.commands[1:]:
            accumulator += segment.outer_box
        return accumulator

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit polygon command."""
        visitor.on_shape(self)

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

    @classmethod
    def new_cw_arc(
        cls,
        start: tuple[float, float],
        end: tuple[float, float],
        center: tuple[float, float],
        thickness: float,
        *,
        negative: bool,
    ) -> Self:
        """Create polygon in shape of circle."""
        start_vector = Vector.from_tuple(start)
        extend_start_vector = start_vector.normalized() * (thickness / 2)

        end_vector = Vector.from_tuple(end)
        extend_end_vector = end_vector.normalized() * (thickness / 2)

        center_vector = Vector.from_tuple(center)

        return cls(
            commands=[
                Arc(
                    start=start_vector + extend_start_vector,
                    end=end_vector + extend_end_vector,
                    center=center_vector,
                    clockwise=True,
                ),
                Arc(
                    start=end_vector - extend_end_vector,
                    end=start_vector - extend_start_vector,
                    center=center_vector,
                    clockwise=False,
                ),
            ],
            negative=negative,
        )
