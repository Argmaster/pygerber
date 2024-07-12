from __future__ import annotations

from pygerber.vm.commands.layer import EndLayer, StartLayer
from pygerber.vm.commands.polygon import Line, Polygon
from pygerber.vm.pillow.vm import PillowVirtualMachine
from pygerber.vm.types.box import Box


def test_draw_rectangle() -> None:
    """Test drawing a rectangle."""
    # Given
    commands = [
        StartLayer.new("main", Box.new((0, 0), 2, 2)),
        Polygon(
            commands=[
                Line.from_tuples((0, 0), (1, 0)),
                Line.from_tuples((1, 0), (1, 1)),
                Line.from_tuples((1, 1), (0, 1)),
                Line.from_tuples((0, 1), (0, 0)),
            ]
        ),
        EndLayer(),
    ]
    PillowVirtualMachine(200).run(commands)
