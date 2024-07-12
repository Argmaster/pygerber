from __future__ import annotations

import inspect
from typing import Sequence

from pygerber.vm.commands.command import Command
from pygerber.vm.commands.layer import EndLayer, StartLayer
from pygerber.vm.commands.polygon import Polygon
from pygerber.vm.pillow.vm import PillowVirtualMachine
from pygerber.vm.types.box import Box
from test.conftest import TEST_DIRECTORY

OUTPUT_PILLOW_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "pillow"
OUTPUT_PILLOW_DIRECTORY.mkdir(parents=True, exist_ok=True)


def run_save_compare(dpmm: int, commands: Sequence[Command]) -> None:
    output_image = PillowVirtualMachine(dpmm).run(commands).get_image()
    caller_name = inspect.stack()[1].function
    save_destination = OUTPUT_PILLOW_DIRECTORY / f"{caller_name}.png"
    output_image.save(save_destination.as_posix())


def test_draw_rectangle_in_center() -> None:
    """Test drawing a rectangle."""
    # Given
    commands = [
        StartLayer.new("main", Box.new((5, 5), 15, 10)),
        Polygon.new_rectangle((5, 5), 2, 1, negative=False),
        EndLayer(),
    ]
    run_save_compare(100, commands)


def test_draw_circle_in_center() -> None:
    """Test drawing a circle."""
    # Given
    commands = [
        StartLayer.new("main", Box.new((5, 5), 15, 10)),
        Polygon.new_circle((5, 5), 2, negative=False),
        EndLayer(),
    ]
    run_save_compare(100, commands)
