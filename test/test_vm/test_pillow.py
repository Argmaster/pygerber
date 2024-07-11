from __future__ import annotations

from pygerber.vm.commands.layer import EndLayer, StartLayer
from pygerber.vm.commands.polygon import Line, Polygon
from pygerber.vm.pillow import PillowVirtualMachine
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.point import Point


def test_draw_rectangle() -> None:
    """Test drawing a rectangle."""
    # Given
    commands = [
        StartLayer(id=LayerID(id="Layer0")),
        Polygon(
            commands=[
                Line(start=Point(x=0, y=0), end=Point(x=1, y=0)),
                Line(start=Point(x=1, y=0), end=Point(x=1, y=1)),
                Line(start=Point(x=1, y=1), end=Point(x=0, y=1)),
                Line(start=Point(x=0, y=1), end=Point(x=0, y=0)),
            ]
        ),
        EndLayer(),
    ]
    PillowVirtualMachine().run(commands)
