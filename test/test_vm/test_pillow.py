from __future__ import annotations

import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence

import pytest
from PIL import Image

from pygerber.vm import RVMC
from pygerber.vm.commands import Command, EndLayer, Shape
from pygerber.vm.pillow import PillowVirtualMachine
from pygerber.vm.types import Box, Style, Vector
from test.conftest import TEST_DIRECTORY
from test.test_builder.test_rvmc import (
    build_main_origin_x_y_layer_origin_x_y_paste_x_y,
    build_main_origin_x_y_layer_origin_x_y_paste_x_y_no_main_origin_mark,
)
from test.test_vm.command_builders import (
    make_circle_in_center_fixed_canvas,
    make_circle_over_circle_in_center_fixed_canvas,
    make_main_layer,
    make_obround_horizontal_in_center_fixed_canvas,
    make_obround_vertical_in_center_fixed_canvas,
    make_paste_circle_over_circle_in_center_fixed_canvas,
    make_paste_circle_over_paste_circle_in_center_dynamic_canvas,
    make_paste_negative_rectangle_in_center_fixed_canvas,
    make_paste_rectangle_in_center_fixed_canvas,
    make_rectangle_in_center_fixed_canvas,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


OUTPUT_PILLOW_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "pillow"
OUTPUT_PILLOW_DIRECTORY.mkdir(parents=True, exist_ok=True)


REFERENCE_ASSETS_DIRECTORY = Path(__file__).parent / "test_pillow_assets"


def run(dpmm: int, commands: Sequence[Command]) -> Image.Image:
    return run_rvmc(dpmm, RVMC(commands=commands))


def run_rvmc(dpmm: int, rvmc: RVMC) -> Image.Image:
    return (
        PillowVirtualMachine(dpmm).run(rvmc).get_image(style=Style.presets.BLACK_WHITE)
    )


def compare(image: Image.Image) -> None:
    caller_name = inspect.stack()[1].function
    save_destination = OUTPUT_PILLOW_DIRECTORY / f"{caller_name}.png"
    image.save(save_destination.as_posix())

    reference_image_path = REFERENCE_ASSETS_DIRECTORY / f"{caller_name}.png"
    if reference_image_path.is_file():
        reference_image = Image.open(reference_image_path)
        if image.convert("RGBA") != reference_image.convert("RGBA"):
            raise AssertionError(image.size, reference_image.size)
    else:
        pytest.skip(f"Reference image not found: {reference_image_path}")


def test_draw_rectangle_in_center() -> None:
    commands = make_rectangle_in_center_fixed_canvas()
    compare(run(100, commands))


def test_draw_obround_horizontal_in_center() -> None:
    commands = make_obround_horizontal_in_center_fixed_canvas()
    compare(run(100, commands))


def test_draw_obround_vertical_in_center() -> None:
    commands = make_obround_vertical_in_center_fixed_canvas()
    compare(run(100, commands))


def test_draw_circle_in_center() -> None:
    commands = make_circle_in_center_fixed_canvas()
    compare(run(100, commands))


def test_draw_circle_over_circle_in_center() -> None:
    commands = make_circle_over_circle_in_center_fixed_canvas()
    compare(run(100, commands))


def test_paste_circle_over_circle_in_center() -> None:
    compare(run_rvmc(100, make_paste_circle_over_circle_in_center_fixed_canvas()))


def test_paste_circle_over_paste_circle_in_center() -> None:
    compare(
        run_rvmc(100, make_paste_circle_over_paste_circle_in_center_dynamic_canvas())
    )


def test_paste_rectangle_in_center() -> None:
    compare(run(100, make_paste_rectangle_in_center_fixed_canvas()))


def test_paste_negative_rectangle_in_center() -> None:
    compare(run(100, make_paste_negative_rectangle_in_center_fixed_canvas()))


class TestCWArc:
    def axes(self) -> Iterable[Shape]:
        yield Shape.new_rectangle((0, 0), 15, 0.1, is_negative=False)
        yield Shape.new_rectangle((0, 0), 0.1, 15, is_negative=False)

    def template(self, *arc: Shape) -> Sequence[Command]:
        return [
            make_main_layer(Box.from_center_width_height((0, 0), 15, 15)),
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
                    Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_90_180(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_180_270(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_270_360(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    # Half arcs

    def test_0_180(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_90_270(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_180_360(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    def test_270_420(self) -> None:
        compare(
            run(
                10,
                self.template(
                    Shape.new_cw_arc((0, 5), (0, -5), (0, 0), 1, is_negative=False)
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
                        is_negative=False,
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
                        is_negative=False,
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
                        is_negative=False,
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
                        is_negative=False,
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
                        is_negative=False,
                    ),
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        is_negative=False,
                    ),
                    Shape.new_cw_arc(
                        (-self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        is_negative=False,
                    ),
                    Shape.new_cw_arc(
                        (self._45_degrees_vector_x, self._45_degrees_vector_x),
                        (self._45_degrees_vector_x, -self._45_degrees_vector_x),
                        (0, 0),
                        1,
                        is_negative=False,
                    ),
                ),
            )
        )


class TestBox:
    def compare_auto_vs_fixed(
        self,
        *commands: Command,
        fixed_box: Box,
        origin: Optional[Vector] = None,
        dpmm: int = 10,
    ) -> None:
        auto_size_image = run(
            dpmm,
            [
                make_main_layer(None, origin),
                *commands,
                EndLayer(),
            ],
        )
        fix_size_image = run(
            dpmm,
            [
                make_main_layer(fixed_box, origin),
                *commands,
                EndLayer(),
            ],
        )
        if auto_size_image != fix_size_image:
            caller_name = inspect.stack()[1].function
            auto_size_image.save(
                (OUTPUT_PILLOW_DIRECTORY / f"TestBox_{caller_name}_auto.png").as_posix()
            )
            fix_size_image.save(
                (
                    OUTPUT_PILLOW_DIRECTORY / f"TestBox_{caller_name}_fixed.png"
                ).as_posix()
            )

            pytest.fail("Images are different")

    def test_two_circle(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_circle((5, 5), 2, is_negative=False),
            Shape.new_circle((0, 0), 2, is_negative=False),
            fixed_box=Box.from_center_width_height((2.5, 2.5), 7, 7),
            origin=Vector(x=2.5, y=2.5),
        )

    def test_two_rectangles(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_rectangle((5, 5), 2, 2, is_negative=False),
            Shape.new_rectangle((0, 0), 2, 2, is_negative=False),
            fixed_box=Box.from_center_width_height((2.5, 2.5), 7, 7),
            origin=Vector(x=2.5, y=2.5),
        )

    def test_circle_rectangle(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_circle((5, 5), 2, is_negative=False),
            Shape.new_rectangle((0, 0), 2, 2, is_negative=False),
            fixed_box=Box.from_center_width_height((2.5, 2.5), 7, 7),
            origin=Vector(x=2.5, y=2.5),
        )

    def test_cw_arc_0_90(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((2.75, -2.75), 5.5, 5.5),
            origin=Vector(x=2.75, y=-2.75),
        )

    def test_cw_arc_90_180(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((-2.75, -2.75), 5.5, 5.5),
            origin=Vector(x=-2.75, y=-2.75),
        )

    def test_cw_arc_180_270(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((-2.75, 2.75), 5.5, 5.5),
            origin=Vector(x=-2.75, y=2.75),
        )

    def test_cw_arc_270_360(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((2.75, 2.75), 5.5, 5.5),
            origin=Vector(x=2.75, y=2.75),
        )

    def test_cw_arc_0_180(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((0, -2.75), 11, 5.5),
            origin=Vector(x=0, y=-2.75),
        )

    def test_cw_arc_90_270(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((-2.75, 0), 5.5, 11),
            origin=Vector(x=-2.75, y=0),
        )

    def test_cw_arc_180_360(self) -> None:
        self.compare_auto_vs_fixed(
            Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, is_negative=False),
            fixed_box=Box.from_center_width_height((0, 2.75), 11, 5.5),
            origin=Vector(x=0, y=2.75),
        )


class TestPasteWithOffset:
    def test_main_origin_0_0_layer_origin_0_0_paste_0_0_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(0, 0)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_0_0_paste_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(2, 2)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_0_0_paste_8_8_expect_circle_at_8_8(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(8, 8)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_2_2_paste_0_0_expect_circle_at_neg_2_neg_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(2, 2), paste=(0, 0)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_2_2_paste_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(2, 2), paste=(2, 2)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_8_8_paste_8_8_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(8, 8), paste=(8, 8)
                ),
            )
        )

    def test_main_origin_2_2_layer_origin_0_0_paste_0_0_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(0, 0), paste=(0, 0)
                ),
            )
        )

    def test_main_origin_2_2_layer_origin_0_0_paste_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(0, 0), paste=(2, 2)
                ),
            )
        )

    def test_main_origin_2_2_layer_origin_2_2_paste_0_0_expect_circle_at_neg_2_neg_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(2, 2), paste=(0, 0)
                ),
            )
        )

    def test_main_origin_2_2_layer_origin_2_2_paste_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(2, 2), paste=(2, 2)
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_0_0_paste_0_0_circle_at_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(0, 0),
                    paste=(0, 0),
                    circle_at=(2, 2),
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_0_0_paste_2_2_circle_at_2_2_expect_circle_at_4_4(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(0, 0),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    def test_main_origin_0_0_layer_origin_2_2_paste_2_2_circle_at_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(2, 2),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    def test_main_origin_neg_8_neg_8_layer_origin_4_4_paste_2_2_circle_at_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(-8, -8),
                    layer_origin=(4, 4),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    def test_main_origin_neg_8_neg_8_layer_origin_4_4_paste_2_2_circle_at_2_2_expect_circle_at_0_0_no_main_origin_mark(
        self,
    ) -> None:
        compare(
            run_rvmc(
                20,
                build_main_origin_x_y_layer_origin_x_y_paste_x_y_no_main_origin_mark(
                    main_origin=(-8, -8),
                    layer_origin=(4, 4),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )
