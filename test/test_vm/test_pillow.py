from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Sequence

from pygerber.vm.commands.command import Command
from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
from pygerber.vm.commands.shape import Shape
from pygerber.vm.pillow.vm import PillowVirtualMachine
from pygerber.vm.types.box import FixedBox
from test.conftest import TEST_DIRECTORY

if TYPE_CHECKING:
    from collections.abc import Iterable

    from PIL import Image

OUTPUT_PILLOW_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "pillow"
OUTPUT_PILLOW_DIRECTORY.mkdir(parents=True, exist_ok=True)


def run(dpmm: int, commands: Sequence[Command]) -> Image.Image:
    return PillowVirtualMachine(dpmm).run(commands).get_image()


def save(image: Image.Image) -> None:
    caller_name = inspect.stack()[1].function
    save_destination = OUTPUT_PILLOW_DIRECTORY / f"{caller_name}.png"
    image.save(save_destination.as_posix())


def test_draw_rectangle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_rectangle((5, 5), 2, 1, negative=False),
        EndLayer(),
    ]
    save(run(100, commands))


def test_draw_circle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_circle((5, 5), 2, negative=False),
        EndLayer(),
    ]
    save(run(100, commands))


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
    save(run(100, commands))


class TestCWArc:
    def axes(self) -> Iterable[Shape]:
        yield Shape.new_rectangle((0, 0), 15, 0.1, negative=False)
        yield Shape.new_rectangle((0, 0), 0.1, 15, negative=False)

    def template(self, *arc: Shape) -> Sequence[Command]:
        return [
            StartLayer.new("main", FixedBox.new((0, 0), 15, 15)),
            *self.axes(),
            *arc,
            EndLayer(),
        ]

    # Quarter arcs

    def test_0_90(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_90_180(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_180_270(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_270_360(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    # Half arcs

    def test_0_180(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_90_270(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_180_360(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_270_420(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, 5), (0, -5), (0, 0), 1, negative=False)
                ),
            )
        )

    # Quarter arcs with 1/8 rotation

    _45_degrees_vector_x = 3.5355339059327378

    def test_45_135(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc(
                        (self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (-self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    )
                ),
            )
        )

    def test_135_225(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    )
                ),
            )
        )

    def test_225_315(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    )
                ),
            )
        )

    def test_315_405(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc(
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    )
                ),
            )
        )

    def test_full_circle_with_quarter_arcs(self) -> None:
        save(
            run(
                10,
                self.template(
                    Shape.new_cw_arc(
                        (self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (-self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    ),
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    ),
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    ),
                    Shape.new_cw_arc(
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        negative=False,
                    ),
                ),
            )
        )
