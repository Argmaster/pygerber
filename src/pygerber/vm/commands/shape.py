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


from abc import ABC, abstractmethod
from typing import Any, Protocol


class DrawingBackend(Protocol):
    def draw_line(self, start: Vector, end: Vector) -> None:
        ...

    def draw_arc(self, start: Vector, end: Vector, center: Vector, clockwise: bool) -> None:
        ...

    def draw_rectangle(self, center: Vector, width: float, height: float) -> None:
        ...

    def draw_circle(self, center: Vector, diameter: float) -> None:
        ...

    def draw_polygon(self, points: list[Vector]) -> None:
        ...


class ShapeType(ABC):
    @abstractmethod
    def draw(self, backend: DrawingBackend) -> None:
        pass


class Line(ShapeType):
    def __init__(self, start: Vector, end: Vector):
        self.start = start
        self.end = end

    def draw(self, backend: DrawingBackend) -> None:
        backend.draw_line(self.start, self.end)


class Arc(ShapeType):
    def __init__(self, start: Vector, end: Vector, center: Vector, clockwise: bool):
        self.start = start
        self.end = end
        self.center = center
        self.clockwise = clockwise

    def draw(self, backend: DrawingBackend) -> None:
        backend.draw_arc(self.start, self.end, self.center, self.clockwise)


class Rectangle(ShapeType):
    def __init__(self, center: Vector, width: float, height: float):
        self.center = center
        self.width = width
        self.height = height

    def draw(self, backend: DrawingBackend) -> None:
        backend.draw_rectangle(self.center, self.width, self.height)


class Circle(ShapeType):
    def __init__(self, center: Vector, diameter: float):
        self.center = center
        self.diameter = diameter

    def draw(self, backend: DrawingBackend) -> None:
        backend.draw_circle(self.center, self.diameter)


class Polygon(ShapeType):
    def __init__(self, points: list[Vector]):
        self.points = points

    def draw(self, backend: DrawingBackend) -> None:
        backend.draw_polygon(self.points)


    """`Shape` command instructs VM to render a shape described by series of
    lines and arcs into currently active layer.

    Last point of first segment (line or arc) is always connected to the first point
    first segment, so shapes are implicitly closed. If those points are not overlapping,
    they are connected by a straight line.
    """

    shape: ShapeType = Field(...)
    is_negative: bool = False

    def draw(self, backend: DrawingBackend) -> None:
        self.shape.draw(backend)

    @pp.cached_property
    is_negative: bool = False

    @pp.cached_property
    def outer_box(self) -> Box:
        if isinstance(self.shape, (Line, Arc)):
            return Box.from_vectors(self.shape.start, self.shape.end)
        elif isinstance(self.shape, Rectangle):
            half_width = self.shape.width / 2
            half_height = self.shape.height / 2
            return Box.from_vectors(
                self.shape.center + Vector(-half_width, -half_height),
                self.shape.center + Vector(half_width, half_height)
            )
        elif isinstance(self.shape, Circle):
            radius = self.shape.diameter / 2
            return Box.from_vectors(
                self.shape.center + Vector(-radius, -radius),
                self.shape.center + Vector(radius, radius)
            )
        elif isinstance(self.shape, Polygon):
            return Box.from_vectors(*self.shape.points)
        else:
            raise NotImplementedError(f"Unsupported shape type: {type(self.shape)}")
        """Get outer box of shape segment."""
        accumulator = self.commands[0].outer_box
        for segment in self.commands[1:]:
            accumulator += segment.outer_box
        return accumulator

    def transform(self, transform: Matrix3x3) -> Self:
        if isinstance(self.shape, (Line, Arc)):
            new_shape = type(self.shape)(
                start=self.shape.start.transform(transform),
                end=self.shape.end.transform(transform),
                center=self.shape.center.transform(transform) if isinstance(self.shape, Arc) else None,
                clockwise=self.shape.clockwise if isinstance(self.shape, Arc) else None
            )
        elif isinstance(self.shape, (Rectangle, Circle)):
            new_shape = type(self.shape)(
                center=self.shape.center.transform(transform),
                width=self.shape.width if isinstance(self.shape, Rectangle) else None,
                height=self.shape.height if isinstance(self.shape, Rectangle) else None,
                diameter=self.shape.diameter if isinstance(self.shape, Circle) else None
            )
        elif isinstance(self.shape, Polygon):
            new_shape = Polygon([point.transform(transform) for point in self.shape.points])
        else:
            raise NotImplementedError(f"Unsupported shape type: {type(self.shape)}")

        return self.__class__(shape=new_shape, is_negative=self.is_negative)
        """Transpose shape by vector."""
        return self.__class__(
            commands=[segment.transform(transform) for segment in self.commands],
            is_negative=self.is_negative,
        )

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit polygon command."""
        visitor.on_shape(self)

    @classmethod
    @classmethod
    def new_rectangle(cls, center: tuple[float, float], width: float, height: float, *, is_negative: bool) -> Self:
        return cls(shape=Rectangle(Vector.from_tuple(center), width, height), is_negative=is_negative)

    @classmethod
    def new_obround(cls, center: tuple[float, float], width: float, height: float, *, is_negative: bool) -> Self:
        # Implement obround as a combination of rectangle and two circles
        if width <= height:
            rect_height = height - width
            circle_diameter = width
            circle1_center = Vector.from_tuple(center) + Vector(0, rect_height / 2)
            circle2_center = Vector.from_tuple(center) - Vector(0, rect_height / 2)
        else:
            rect_width = width - height
            circle_diameter = height
            circle1_center = Vector.from_tuple(center) + Vector(rect_width / 2, 0)
            circle2_center = Vector.from_tuple(center) - Vector(rect_width / 2, 0)

        return cls(
            shape=Polygon([
                Rectangle(Vector.from_tuple(center), min(width, height), max(width, height)),
                Circle(circle1_center, circle_diameter),
                Circle(circle2_center, circle_diameter)
            ]),
            is_negative=is_negative
        )

    @classmethod
    def new_circle(cls, center: tuple[float, float], diameter: float, *, is_negative: bool) -> Self:
        return cls(shape=Circle(Vector.from_tuple(center), diameter), is_negative=is_negative)

    @classmethod
    def new_polygon(cls, center: tuple[float, float], outer_diameter: float, vertices_count: int, base_rotation: float, *, is_negative: bool) -> Self:
        points = []
        for i in range(vertices_count):
            angle = base_rotation + i * (360 / vertices_count)
            point = Vector.from_tuple(center) + Vector.from_polar(outer_diameter / 2, angle)
            points.append(point)
        return cls(shape=Polygon(points), is_negative=is_negative)

    @classmethod
    def new_line(cls, start: tuple[float, float], end: tuple[float, float], thickness: float, *, is_negative: bool) -> Self:
        return cls(shape=Line(Vector.from_tuple(start), Vector.from_tuple(end)), is_negative=is_negative)

    @classmethod
    def new_cw_arc(cls, start: tuple[float, float], end: tuple[float, float], center: tuple[float, float], thickness: float, *, is_negative: bool) -> Self:
        return cls(shape=Arc(Vector.from_tuple(start), Vector.from_tuple(end), Vector.from_tuple(center), clockwise=True), is_negative=is_negative)

    @classmethod
    def new_ccw_arc(cls, start: tuple[float, float], end: tuple[float, float], center: tuple[float, float], thickness: float, *, is_negative: bool) -> Self:
        return cls(shape=Arc(Vector.from_tuple(start), Vector.from_tuple(end), Vector.from_tuple(center), clockwise=False), is_negative=is_negative)

    @classmethod
    def new_ring(cls, center: tuple[float, float], outer_diameter: float, inner_diameter: float, *, is_negative: bool) -> tuple[Self, Self]:
        outer_circle = cls.new_circle(center, outer_diameter, is_negative=is_negative)
        inner_circle = cls.new_circle(center, inner_diameter, is_negative=not is_negative)
        return outer_circle, inner_circle

    @classmethod
    def new_connected_points(cls, *points: tuple[float, float], is_negative: bool) -> Self:
        return cls(shape=Polygon([Vector.from_tuple(p) for p in points]), is_negative=is_negative)
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
