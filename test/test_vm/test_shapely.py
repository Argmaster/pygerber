from __future__ import annotations

import inspect
from pathlib import Path
from typing import Sequence

from pygerber.vm import RVMC
from pygerber.vm.commands import Command
from pygerber.vm.shapely import ShapelyVirtualMachine
from pygerber.vm.shapely.vm import ShapelyResult
from test.conftest import TEST_DIRECTORY
from test.test_vm.command_builders import (
    make_circle_in_center_fixed_canvas,
    make_circle_over_circle_in_center_fixed_canvas,
    make_intersecting_circle_circle,
    make_intersecting_circle_circle_negative,
    make_intersecting_cross_0_0_circle_5_5,
    make_intersecting_rectangle_circle,
    make_intersecting_rectangles_2_dynamic_canvas,
    make_intersecting_rectangles_dynamic_canvas,
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


def test_draw_rectangle_in_center() -> None:
    save(run(make_rectangle_in_center_fixed_canvas()))


def test_draw_obround_horizontal_in_center() -> None:
    save(run(make_obround_horizontal_in_center_fixed_canvas()))


def test_draw_obround_vertical_in_center() -> None:
    save(run(make_obround_vertical_in_center_fixed_canvas()))


def test_draw_circle_in_center() -> None:
    save(run(make_circle_in_center_fixed_canvas()))


def test_draw_circle_over_circle_in_center() -> None:
    save(run(make_circle_over_circle_in_center_fixed_canvas()))


def test_paste_circle_over_circle_in_center() -> None:
    save(run_rvmc(make_paste_circle_over_circle_in_center_fixed_canvas()))


def test_paste_circle_over_paste_circle_in_center() -> None:
    save(run_rvmc(make_paste_circle_over_paste_circle_in_center_dynamic_canvas()))


def test_paste_rectangle_in_center() -> None:
    save(run(make_paste_rectangle_in_center_fixed_canvas()))


def test_paste_negative_rectangle_in_center() -> None:
    save(run(make_paste_negative_rectangle_in_center_fixed_canvas()))


def test_intersecting_rectangles_dynamic_canvas() -> None:
    save(run_rvmc(make_intersecting_rectangles_dynamic_canvas()))


def test_intersecting_rectangles_2_dynamic_canvas() -> None:
    save(run_rvmc(make_intersecting_rectangles_2_dynamic_canvas()))


def test_intersecting_rectangle_circle() -> None:
    save(run_rvmc(make_intersecting_rectangle_circle()))


def test_intersecting_circle_circle() -> None:
    save(run_rvmc(make_intersecting_circle_circle()))


def test_intersecting_circle_circle_negative() -> None:
    save(run_rvmc(make_intersecting_circle_circle_negative()))


def test_intersecting_cross_0_0_circle_5_5() -> None:
    save(run_rvmc(make_intersecting_cross_0_0_circle_5_5()))
