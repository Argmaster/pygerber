"""`shape` module contains classes for drawing shapes consisting of connected lines
and arcs filled with solid color.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

import pyparsing as pp
from pydantic import Field

from pygerber.vm.commands.command import Command
from pygerber.vm.commands.shape_segments import Arc, Line, ShapeSegment
from pygerber.vm.types.box import Box
from pygerber.vm.types.matrix import Matrix3x3
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.vm.vm import CommandVisitor


FULL_ANGLE_DEGREES = 360
VERTEX_COUNT_IN_TRIANGLE = 3


class Shape(Command):
    """`Shape` command instructs VM to render a shape described by series of
    lines and arcs into currently active layer.

    Last point of first segment (line or arc) is always connected to the first point
    first segment, so shapes are implicitly closed. If those points are not overlapping,
    they are connected by a straight line.
    """

    commands: List[ShapeSegment] = Field(min_length=1)
    is_negative: bool = False

    @pp.cached_property
    def outer_box(self) -> Box:
        """Get outer box of shape segment."""
        accumulator = self.commands[0].outer_box
        for segment in self.commands[1:]:
            accumulator += segment.outer_box
        return accumulator

    def transform(self, transform: Matrix3x3) -> Self:
        """Transpose shape by vector."""
        return self.__class__(
            commands=[segment.transform(transform) for segment in self.commands],
            is_negative=self.is_negative,
        )

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit polygon command."""
        visitor.on_shape(self)

    @classmethod
    def new_rectangle(
        cls,
        center: tuple[float, float],
        width: float,
        height: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of rectangle."""
        half_height = height / 2
        half_width = width / 2
        return cls(
            commands=[
                # Bottom line
                Line.from_tuples(
                    (center[0] - half_width, center[1] - half_height),
                    (center[0] + half_width, center[1] - half_height),
                ),
                # Right line
                Line.from_tuples(
                    (center[0] + half_width, center[1] - half_height),
                    (center[0] + half_width, center[1] + half_height),
                ),
                # Top line
                Line.from_tuples(
                    (center[0] + half_width, center[1] + half_height),
                    (center[0] - half_width, center[1] + half_height),
                ),
                # Left line
                Line.from_tuples(
                    (center[0] - half_width, center[1] + half_height),
                    (center[0] - half_width, center[1] - half_height),
                ),
            ],
            is_negative=is_negative,
        )

    @classmethod
    def new_obround(
        cls,
        center: tuple[float, float],
        width: float,
        height: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of rectangle with shorter side rounded."""
        half_height = height / 2
        half_width = width / 2

        if width <= height:
            # Shape is taller than wider, hence rounding should be on bottom and top
            delta = half_width

            return cls(
                commands=[
                    # Bottom arc
                    Arc.from_tuples(
                        (center[0] - half_width, center[1] - half_height + delta),
                        (center[0] + half_width, center[1] - half_height + delta),
                        (center[0], center[1] - half_height + delta),
                        clockwise=False,
                    ),
                    # Right line
                    Line.from_tuples(
                        (center[0] + half_width, center[1] - half_height + delta),
                        (center[0] + half_width, center[1] + half_height - delta),
                    ),
                    # Top arc
                    Arc.from_tuples(
                        (center[0] + half_width, center[1] + half_height - delta),
                        (center[0] - half_width, center[1] + half_height - delta),
                        (center[0], center[1] + half_height - delta),
                        clockwise=False,
                    ),
                    # Left line
                    Line.from_tuples(
                        (center[0] - half_width, center[1] + half_height - delta),
                        (center[0] - half_width, center[1] - half_height + delta),
                    ),
                ],
                is_negative=is_negative,
            )

        delta = half_height
        return cls(
            commands=[
                # Bottom line
                Line.from_tuples(
                    (center[0] - half_width + delta, center[1] - half_height),
                    (center[0] + half_width - delta, center[1] - half_height),
                ),
                # Right line
                Arc.from_tuples(
                    (center[0] + half_width - delta, center[1] - half_height),
                    (center[0] + half_width - delta, center[1] + half_height),
                    (center[0] + half_width - delta, center[1]),
                    clockwise=False,
                ),
                # Top line
                Line.from_tuples(
                    (center[0] + half_width - delta, center[1] + half_height),
                    (center[0] - half_width + delta, center[1] + half_height),
                ),
                # Left line
                Arc.from_tuples(
                    (center[0] - half_width + delta, center[1] + half_height),
                    (center[0] - half_width + delta, center[1] - half_height),
                    (center[0] - half_width + delta, center[1]),
                    clockwise=False,
                ),
            ],
            is_negative=is_negative,
        )

    @classmethod
    def new_circle(
        cls, center: tuple[float, float], diameter: float, *, is_negative: bool
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
            is_negative=is_negative,
        )

    @classmethod
    def new_polygon(
        cls,
        center: tuple[float, float],
        outer_diameter: float,
        vertices_count: int,
        base_rotation: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of regular polygon."""
        assert vertices_count >= VERTEX_COUNT_IN_TRIANGLE
        base_rotation = base_rotation % 360
        assert 0 <= base_rotation < FULL_ANGLE_DEGREES

        center_vector = Vector.from_tuple(center)
        commands: list[ShapeSegment] = []

        angle_step = 360 / vertices_count
        transform_matrix = Matrix3x3.new_rotate(angle_step)

        local_vertex_offset = Vector.unit.x * outer_diameter / 2
        local_vertex_offset = local_vertex_offset.transform(
            Matrix3x3.new_rotate(base_rotation)
        )
        current_angle = base_rotation

        while current_angle < FULL_ANGLE_DEGREES:
            current_angle += angle_step
            new_local_vertex_offset = local_vertex_offset.transform(transform_matrix)

            commands.append(
                Line(
                    start=center_vector + local_vertex_offset,
                    end=center_vector + new_local_vertex_offset,
                )
            )
            local_vertex_offset = new_local_vertex_offset

        return cls(commands=commands, is_negative=is_negative)

    @classmethod
    def new_line(
        cls,
        start: tuple[float, float],
        end: tuple[float, float],
        thickness: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of line with specified thickness."""
        start_vector = Vector.from_tuple(start)
        end_vector = Vector.from_tuple(end)
        parallel = (end_vector - start_vector).normalized()
        perpendicular = Vector(x=-parallel.y, y=parallel.x) * (thickness / 2)

        return cls(
            commands=[
                Line(
                    start=start_vector + perpendicular,
                    end=end_vector + perpendicular,
                ),
                Line(
                    start=end_vector - perpendicular,
                    end=start_vector - perpendicular,
                ),
            ],
            is_negative=is_negative,
        )

    @classmethod
    def new_cw_arc(
        cls,
        start: tuple[float, float],
        end: tuple[float, float],
        center: tuple[float, float],
        thickness: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of clockwise arc with specified thickness."""
        center_vector = Vector.from_tuple(center)
        start_vector = Vector.from_tuple(start)
        end_vector = Vector.from_tuple(end)

        local_start_vector = start_vector - Vector.from_tuple(center)
        extend_start_vector = local_start_vector.normalized() * (thickness / 2)

        local_end_vector = end_vector - Vector.from_tuple(center)
        extend_end_vector = local_end_vector.normalized() * (thickness / 2)

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
            is_negative=is_negative,
        )

    @classmethod
    def new_ccw_arc(
        cls,
        start: tuple[float, float],
        end: tuple[float, float],
        center: tuple[float, float],
        thickness: float,
        *,
        is_negative: bool,
    ) -> Self:
        """Create polygon in shape of counterclockwise arc with specified thickness."""
        return cls.new_cw_arc(
            start=end,
            end=start,
            center=center,
            thickness=thickness,
            is_negative=is_negative,
        )

    @classmethod
    def new_ring(
        cls,
        center: tuple[float, float],
        outer_diameter: float,
        inner_diameter: float,
        *,
        is_negative: bool,
    ) -> tuple[Self, Self]:
        """Create polygon in shape of ring."""
        thickness = (outer_diameter - inner_diameter) / 2
        inner_radius = inner_diameter / 2

        assert thickness > 0
        assert inner_radius > 0

        half_thickness = thickness / 2

        point_0 = (center[0] + inner_radius + half_thickness, center[1])
        point_1 = (center[0] - inner_radius - half_thickness, center[1])

        return (
            cls.new_cw_arc(
                point_0,
                point_1,
                center,
                thickness=thickness,
                is_negative=is_negative,
            ),
            cls.new_cw_arc(
                point_1,
                point_0,
                center,
                thickness=thickness,
                is_negative=is_negative,
            ),
        )

    @classmethod
    def new_connected_points(
        cls, *points: tuple[float, float], is_negative: bool
    ) -> Self:
        """Create polygon from connected points."""
        commands: list[ShapeSegment] = [
            Line.from_tuples(points[i], points[i + 1]) for i in range(len(points) - 1)
        ]
        commands.append(Line.from_tuples(points[-1], points[0]))
        return cls(commands=commands, is_negative=is_negative)
