from __future__ import annotations

import inspect
from pathlib import Path
from typing import Iterable, Sequence

from pygerber.vm import RVMC
from pygerber.vm.commands import Command
from pygerber.vm.commands.layer import EndLayer
from pygerber.vm.commands.shape import Shape
from pygerber.vm.shapely import ShapelyVirtualMachine
from pygerber.vm.shapely.vm import ShapelyResult
from pygerber.vm.types.box import Box
from test.conftest import TEST_DIRECTORY
from test.tags import Tag, tag
from test.test_builder.test_rvmc import (
    build_main_origin_x_y_layer_origin_x_y_paste_x_y,
    build_main_origin_x_y_layer_origin_x_y_paste_x_y_no_main_origin_mark,
)
from test.unit.test_vm.command_builders import (
    make_circle_in_center_fixed_canvas,
    make_circle_over_circle_in_center_fixed_canvas,
    make_intersecting_circle_circle,
    make_intersecting_circle_circle_negative,
    make_intersecting_cross_0_0_circle_5_5,
    make_intersecting_rectangle_circle,
    make_intersecting_rectangles_2_dynamic_canvas,
    make_intersecting_rectangles_dynamic_canvas,
    make_main_layer,
    make_obround_horizontal_in_center_fixed_canvas,
    make_obround_vertical_in_center_fixed_canvas,
    make_paste_circle_over_circle_in_center_fixed_canvas,
    make_paste_circle_over_paste_circle_in_center_dynamic_canvas,
    make_paste_negative_rectangle_in_center_fixed_canvas,
    make_paste_rectangle_in_center_fixed_canvas,
    make_rectangle_in_center_fixed_canvas,
)

OUTPUT_SHAPELY_DIRECTORY = TEST_DIRECTORY / ".vm-output" / "shapely"
OUTPUT_SHAPELY_DIRECTORY.mkdir(parents=True, exist_ok=True)


REFERENCE_ASSETS_DIRECTORY = Path(__file__).parent / "test_shapely_assets"


def run(commands: Sequence[Command]) -> ShapelyResult:
    return run_rvmc(RVMC(commands=commands))


def run_rvmc(rvmc: RVMC) -> ShapelyResult:
    return ShapelyVirtualMachine().run(rvmc)


def save(result: ShapelyResult) -> None:
    caller_name = inspect.stack()[1].function
    result.save_svg((OUTPUT_SHAPELY_DIRECTORY / caller_name).with_suffix(".svg"))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_draw_rectangle_in_center() -> None:
    save(run(make_rectangle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_draw_obround_horizontal_in_center() -> None:
    save(run(make_obround_horizontal_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_draw_obround_vertical_in_center() -> None:
    save(run(make_obround_vertical_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_draw_circle_in_center() -> None:
    save(run(make_circle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_draw_circle_over_circle_in_center() -> None:
    save(run(make_circle_over_circle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_paste_circle_over_circle_in_center() -> None:
    save(run_rvmc(make_paste_circle_over_circle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_paste_circle_over_paste_circle_in_center() -> None:
    save(run_rvmc(make_paste_circle_over_paste_circle_in_center_dynamic_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_paste_rectangle_in_center() -> None:
    save(run(make_paste_rectangle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_paste_negative_rectangle_in_center() -> None:
    save(run(make_paste_negative_rectangle_in_center_fixed_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_rectangles_dynamic_canvas() -> None:
    save(run_rvmc(make_intersecting_rectangles_dynamic_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_rectangles_2_dynamic_canvas() -> None:
    save(run_rvmc(make_intersecting_rectangles_2_dynamic_canvas()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_rectangle_circle() -> None:
    save(run_rvmc(make_intersecting_rectangle_circle()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_circle_circle() -> None:
    save(run_rvmc(make_intersecting_circle_circle()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_circle_circle_negative() -> None:
    save(run_rvmc(make_intersecting_circle_circle_negative()))


@tag(Tag.SHAPELY, Tag.EXTRAS)
def test_intersecting_cross_0_0_circle_5_5() -> None:
    save(run_rvmc(make_intersecting_cross_0_0_circle_5_5()))


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

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_0_90(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((5, 0), (0, -5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_90_180(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((0, -5), (-5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_180_270(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((-5, 0), (0, 5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_270_360(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((0, 5), (5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    # Half arcs

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_0_180(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((5, 0), (-5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_90_270(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((0, -5), (0, 5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_180_360(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((-5, 0), (5, 0), (0, 0), 1, is_negative=False)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_270_420(self) -> None:
        save(
            run(
                self.template(
                    Shape.new_cw_arc((0, 5), (0, -5), (0, 0), 1, is_negative=False)
                ),
            )
        )

    # Quarter arcs with 1/8 rotation

    _45_degrees_vector_x = 3.5355339059327378

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_45_135(self) -> None:
        save(
            run(
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

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_135_225(self) -> None:
        save(
            run(
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

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_225_315(self) -> None:
        save(
            run(
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

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_315_405(self) -> None:
        save(
            run(
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

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_full_circle_with_quarter_arcs(self) -> None:
        save(
            run(
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


class TestPasteWithOffset:
    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_0_0_paste_0_0_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(0, 0)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_0_0_paste_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(2, 2)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_0_0_paste_8_8_expect_circle_at_8_8(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(0, 0), paste=(8, 8)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_2_2_paste_0_0_expect_circle_at_neg_2_neg_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(2, 2), paste=(0, 0)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_2_2_paste_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(2, 2), paste=(2, 2)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_8_8_paste_8_8_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0), layer_origin=(8, 8), paste=(8, 8)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_2_2_layer_origin_0_0_paste_0_0_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(0, 0), paste=(0, 0)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_2_2_layer_origin_0_0_paste_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(0, 0), paste=(2, 2)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_2_2_layer_origin_2_2_paste_0_0_expect_circle_at_neg_2_neg_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(2, 2), paste=(0, 0)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_2_2_layer_origin_2_2_paste_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(2, 2), layer_origin=(2, 2), paste=(2, 2)
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_0_0_paste_0_0_circle_at_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(0, 0),
                    paste=(0, 0),
                    circle_at=(2, 2),
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_0_0_paste_2_2_circle_at_2_2_expect_circle_at_4_4(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(0, 0),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_0_0_layer_origin_2_2_paste_2_2_circle_at_2_2_expect_circle_at_2_2(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(0, 0),
                    layer_origin=(2, 2),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_neg_8_neg_8_layer_origin_4_4_paste_2_2_circle_at_2_2_expect_circle_at_0_0(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y(
                    main_origin=(-8, -8),
                    layer_origin=(4, 4),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )

    @tag(Tag.SHAPELY, Tag.EXTRAS)
    def test_main_origin_neg_8_neg_8_layer_origin_4_4_paste_2_2_circle_at_2_2_expect_circle_at_0_0_no_main_origin_mark(
        self,
    ) -> None:
        save(
            run_rvmc(
                build_main_origin_x_y_layer_origin_x_y_paste_x_y_no_main_origin_mark(
                    main_origin=(-8, -8),
                    layer_origin=(4, 4),
                    paste=(2, 2),
                    circle_at=(2, 2),
                ),
            )
        )
