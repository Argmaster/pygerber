from __future__ import annotations

import pytest

from pygerber.vm.commands import Line
from pygerber.vm.types.box import Box
from pygerber.vm.types.vector import Vector


class TestLine:
    def test_from_tuples(self) -> None:
        assert Line.from_tuples((0.0, 0.0), (1.0, 1.0)) == Line(
            start=Vector(x=0.0, y=0.0), end=Vector(x=1.0, y=1.0)
        )

    @pytest.mark.parametrize("length", [1.0, 2.0, 3.0])
    def test_outer_box_0(self, length: float) -> None:
        line = Line.from_tuples((0.0, 0.0), (length, length))
        assert line.outer_box == Box(min_x=0.0, min_y=0.0, max_x=length, max_y=length)

    @pytest.mark.parametrize("length", [1.0, 2.0, 3.0])
    def test_outer_box_1(self, length: float) -> None:
        line = Line.from_tuples((length, length), (0.0, 0.0))
        assert line.outer_box == Box(min_x=0.0, min_y=0.0, max_x=length, max_y=length)

    @pytest.mark.parametrize("length", [1.0, 2.0, 3.0])
    def test_outer_box_2(self, length: float) -> None:
        line = Line.from_tuples((0.0, length), (length, 0.0))
        assert line.outer_box == Box(min_x=0.0, min_y=0.0, max_x=length, max_y=length)

    @pytest.mark.parametrize("length", [1.0, 2.0, 3.0])
    def test_outer_box_3(self, length: float) -> None:
        line = Line.from_tuples((length, 0.0), (0.0, length))
        assert line.outer_box == Box(min_x=0.0, min_y=0.0, max_x=length, max_y=length)

    @pytest.mark.parametrize("length", [-1.0, -2.0, -3.0])
    def test_outer_box_4(self, length: float) -> None:
        line = Line.from_tuples((0.0, 0.0), (length, length))
        assert line.outer_box == Box(min_x=length, min_y=length, max_x=0.0, max_y=0.0)

    @pytest.mark.parametrize("length", [-1.0, -2.0, -3.0])
    def test_outer_box_5(self, length: float) -> None:
        line = Line.from_tuples((length, length), (0.0, 0.0))
        assert line.outer_box == Box(min_x=length, min_y=length, max_x=0.0, max_y=0.0)

    @pytest.mark.parametrize("length", [-1.0, -2.0, -3.0])
    def test_outer_box_6(self, length: float) -> None:
        line = Line.from_tuples((0.0, length), (length, 0.0))
        assert line.outer_box == Box(min_x=length, min_y=length, max_x=0.0, max_y=0.0)

    @pytest.mark.parametrize("length", [-1.0, -2.0, -3.0])
    def test_outer_box_7(self, length: float) -> None:
        line = Line.from_tuples((length, 0.0), (0.0, length))
        assert line.outer_box == Box(min_x=length, min_y=length, max_x=0.0, max_y=0.0)
