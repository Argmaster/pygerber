from __future__ import annotations

import inspect
from typing import Sequence

from pygerber.vm.commands.command import Command
from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
from pygerber.vm.commands.shape import Shape
from pygerber.vm.pillow.vm import PillowVirtualMachine
from pygerber.vm.types.box import FixedBox
from test.conftest import TEST_DIRECTORY

OUTPUT_PILLOW_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "pillow"
OUTPUT_PILLOW_DIRECTORY.mkdir(parents=True, exist_ok=True)


def run_save_compare(dpmm: int, commands: Sequence[Command]) -> None:
    output_image = PillowVirtualMachine(dpmm).run(commands).get_image()
    caller_name = inspect.stack()[1].function
    save_destination = OUTPUT_PILLOW_DIRECTORY / f"{caller_name}.png"
    output_image.save(save_destination.as_posix())


def test_draw_rectangle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_rectangle((5, 5), 2, 1, negative=False),
        EndLayer(),
    ]
    run_save_compare(100, commands)


def test_draw_circle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_circle((5, 5), 2, negative=False),
        EndLayer(),
    ]
    run_save_compare(100, commands)


def test_paste_rectangle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        StartLayer.new("rect", FixedBox.new((0, 0), 5, 5)),
        Shape.new_rectangle((0, 0), 2, 1, negative=False),
        EndLayer(),
        Shape.new_rectangle((5, 5), 3, 2, negative=False),
        Shape.new_rectangle((5, 5), 2.8, 1.8, negative=True),
        PasteLayer.new("rect", (5, 5), "main"),
        EndLayer(),
    ]
    run_save_compare(100, commands)
