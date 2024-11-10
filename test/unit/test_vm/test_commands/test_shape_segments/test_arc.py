from __future__ import annotations

import math as m

import pytest

from pygerber.vm.commands import Arc
from pygerber.vm.types.box import Box
from pygerber.vm.types.vector import Vector


class ArcParams:
    def __init__(
        self,
        id_str: str,
        rel_start: tuple[float, float],
        rel_end: tuple[float, float],
        center: tuple[float, float],
        clockwise: bool,  # noqa: FBT001
        box: Box,
    ) -> None:
        self.start = (rel_start[0] + center[0], rel_start[1] + center[1])
        self.end = (rel_end[0] + center[0], rel_end[1] + center[1])
        self.center = center
        self.clockwise = clockwise
        self.id_str = id_str
        self.box = box

    def __str__(self) -> str:
        return self.id_str

    __repr__ = __str__


sin45 = m.sqrt(2) / 2


class TestArc:
    def _start(self) -> tuple[float, float]:
        return (0.0 + 2.0, self._length() + 6.0)

    def _end(self) -> tuple[float, float]:
        return (self._length() + 2.0, 0.0 + 6.0)

    def _center(self) -> tuple[float, float]:
        return (2.0, 6.0)

    def _length(self) -> float:
        return 4.0

    def test_from_tuples(self) -> None:
        start = self._start()
        end = self._end()
        center = self._center()
        clockwise = False

        arc = Arc.from_tuples(start, end, center, clockwise=clockwise)

        assert arc.is_valid_arc()
        assert arc.start == Vector.from_tuple(start)
        assert arc.end == Vector.from_tuple(end)
        assert arc.center == Vector.from_tuple(center)
        assert arc.clockwise == clockwise

    def test_get_relative_start_point(self) -> None:
        start = self._start()
        end = self._end()
        center = self._center()
        clockwise = False

        arc = Arc.from_tuples(start, end, center, clockwise=clockwise)

        result = arc.get_relative_start_point()

        assert arc.is_valid_arc()
        assert result == Vector.from_tuple((0.0, 4.0))

    def get_relative_end_point(self) -> None:
        start = self._start()
        end = self._end()
        center = self._center()
        clockwise = False

        arc = Arc.from_tuples(start, end, center, clockwise=clockwise)

        result = arc.get_relative_end_point()

        assert arc.is_valid_arc()
        assert result == Vector.from_tuple((4.0, 0.0))

    def test_get_radius(self) -> None:
        start = self._start()
        end = self._end()
        center = self._center()
        clockwise = False

        arc = Arc.from_tuples(start, end, center, clockwise=clockwise)

        assert arc.is_valid_arc()
        assert arc.get_radius() == self._length()

    @pytest.mark.parametrize(
        ("params"),
        [
            ArcParams(
                "CW 0.0 90.0 (0, 0)",
                (4.0, 0.0),
                (0.0, -4.0),
                (0.0, 0.0),
                clockwise=True,
                box=Box(min_x=0.0, min_y=-4.0, max_x=4.0, max_y=0.0),
            ),
            ArcParams(
                "CCW 0.0 90.0 (0, 0)",
                (4.0, 0.0),
                (0.0, -4.0),
                (0.0, 0.0),
                clockwise=False,
                box=Box(min_x=-4.0, min_y=-4.0, max_x=4.0, max_y=4.0),
            ),
            ArcParams(
                "CW 270.0 0.0 (0, 0)",
                (0.0, 4.0),
                (4.0, 0.0),
                (0.0, 0.0),
                clockwise=True,
                box=Box(min_x=0.0, min_y=0.0, max_x=4.0, max_y=4.0),
            ),
            ArcParams(
                "CCW 270.0 0.0 (0, 0)",
                (0.0, 4.0),
                (4.0, 0.0),
                (0.0, 0.0),
                clockwise=False,
                box=Box(min_x=-4.0, min_y=-4.0, max_x=4.0, max_y=4.0),
            ),
            ArcParams(
                "CW 270.0 0.0 (2, 3)",
                (0.0, 4.0),
                (4.0, 0.0),
                (2.0, 3.0),
                clockwise=True,
                box=Box(min_x=2.0, min_y=3.0, max_x=6.0, max_y=7.0),
            ),
            ArcParams(
                "CCW 270.0 0.0 (2, 3)",
                (0.0, 4.0),
                (4.0, 0.0),
                (2.0, 3.0),
                clockwise=False,
                box=Box(min_x=-2.0, min_y=-1.0, max_x=6.0, max_y=7.0),
            ),
            ArcParams(
                "CW 45.0 315.0 (0, 0)",
                (sin45, -sin45),
                (sin45, sin45),
                (0.0, 0.0),
                clockwise=True,
                box=Box(min_x=-1.0, min_y=-1.0, max_x=sin45, max_y=1.0),
            ),
            ArcParams(
                "CCW 45.0 315.0 (0, 0)",
                (sin45, -sin45),
                (sin45, sin45),
                (0.0, 0.0),
                clockwise=False,
                box=Box(min_x=0.0, min_y=-sin45, max_x=1.0, max_y=sin45),
            ),
        ],
        ids=lambda x: str(x),
    )
    def test_outer_box(
        self,
        params: ArcParams,
    ) -> None:
        arc = Arc.from_tuples(
            params.start, params.end, params.center, clockwise=params.clockwise
        )

        assert arc.is_valid_arc()
        assert arc.outer_box == params.box
