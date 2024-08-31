from __future__ import annotations

import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

import pytest
from PIL import Image

from pygerber.vm.commands import Command, EndLayer, PasteLayer, Shape, StartLayer
from pygerber.vm.pillow.vm import PillowVirtualMachine
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types.box import AutoBox, FixedBox
from test.conftest import TEST_DIRECTORY

if TYPE_CHECKING:
    from collections.abc import Iterable


OUTPUT_PILLOW_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "pillow"
OUTPUT_PILLOW_DIRECTORY.mkdir(parents=True, exist_ok=True)


REFERENCE_ASSETS_DIRECTORY = Path(__file__).parent / "test_pillow_assets"


def run(dpmm: int, commands: Sequence[Command]) -> Image.Image:
    return PillowVirtualMachine(dpmm).run(RVMC(commands)).get_image()


def compare(image: Image.Image) -> None:
    caller_name = inspect.stack()[1].function
    save_destination = OUTPUT_PILLOW_DIRECTORY / f"{caller_name}.png"
    image.save(save_destination.as_posix())

    reference_image_path = REFERENCE_ASSETS_DIRECTORY / f"{caller_name}.png"
    if reference_image_path.is_file():
        reference_image = Image.open(reference_image_path)
        assert image.convert("RGBA") == reference_image.convert("RGBA")
    else:
        pytest.skip(f"Reference image not found: {reference_image_path}")


def test_draw_rectangle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_rectangle((5, 5), 2, 1, negative=False),
        EndLayer(),
    ]
    compare(run(100, commands))


def test_draw_circle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        Shape.new_circle((5, 5), 2, negative=False),
        EndLayer(),
    ]
    compare(run(100, commands))


def test_paste_rectangle_in_center() -> None:
    commands = [
        StartLayer.new("main", FixedBox.new((5, 5), 15, 10)),
        StartLayer.new("rect", FixedBox.new((0, 0), 5, 5)),
        Shape.new_rectangle((0, 0), 2, 1, negative=False),
        EndLayer(),
        Shape.new_rectangle((5, 5), 3, 2, negative=False),
        Shape.new_rectangle((5, 5), 2.8, 1.8, negative=True),
        PasteLayer.new("rect", (5, 5)),
        EndLayer(),
    ]
    compare(run(100, commands))


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
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_90_180(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_180_270(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_270_360(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    # Half arcs

    def test_0_180(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_90_270(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_180_360(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, negative=False)
                ),
            )
        )

    def test_270_420(self) -> None:
        compare(
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
        compare(
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
        compare(
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
        compare(
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
        compare(
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
        compare(
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


class TestAutoBox:
    def compare_auto_vs_fixed(
        self,
        *commands: Command,
        fixed_box: FixedBox,
        dpmm: int = 10,
    ) -> None:
        auto_size_image = run(
            dpmm,
            [
                StartLayer.new("main", AutoBox()),
                *commands,
                EndLayer(),
            ],
        )
        fix_size_image = run(
            dpmm,
            [
                StartLayer.new("main", fixed_box),
                *commands,
                EndLayer(),
            ],
        )
        if auto_size_image != fix_size_image:
            caller_name = inspect.stack()[1].function
            auto_size_image.save(
                (
                    OUTPUT_PILLOW_DIRECTORY / f"TestAutoBox_{caller_name}_auto.png"
                ).as_posix()
            )
            fix_size_image.save(
                (
                    OUTPUT_PILLOW_DIRECTORY / f"TestAutoBox_{caller_name}_fixed.png"
                ).as_posix()
            )

            pytest.fail("Images are different")

    def test_two_circle(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_circle((5, 5), 2, negative=False),
            Shape.new_circle((0, 0), 2, negative=False),
            fixed_box=FixedBox.new((2.5, 2.5), 7, 7),
        )

    def test_two_rectangles(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_rectangle((5, 5), 2, 2, negative=False),
            Shape.new_rectangle((0, 0), 2, 2, negative=False),
            fixed_box=FixedBox.new((2.5, 2.5), 7, 7),
        )

    def test_circle_rectangle(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_circle((5, 5), 2, negative=False),
            Shape.new_rectangle((0, 0), 2, 2, negative=False),
            fixed_box=FixedBox.new((2.5, 2.5), 7, 7),
        )

    def test_cw_arc_0_90(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((2.75, -2.75), 5.5, 5.5),
        )

    def test_cw_arc_90_180(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((-2.75, -2.75), 5.5, 5.5),
        )

    def test_cw_arc_180_270(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((-2.75, 2.75), 5.5, 5.5),
        )

    def test_cw_arc_270_360(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((2.75, 2.75), 5.5, 5.5),
        )

    def test_cw_arc_0_180(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((0, -2.75), 11, 5.5),
        )

    def test_cw_arc_90_270(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((-2.75, 0), 5.5, 11),
        )

    def test_cw_arc_180_360(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, negative=False),
            fixed_box=FixedBox.new((0, 2.75), 11, 5.5),
        )
