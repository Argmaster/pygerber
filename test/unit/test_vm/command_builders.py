from __future__ import annotations

from typing import Optional

from pygerber.builder.rvmc import RvmcBuilder
from pygerber.vm import RVMC
from pygerber.vm.commands import Command, EndLayer, Shape, StartLayer
from pygerber.vm.commands.paste import PasteLayer
from pygerber.vm.types import Box, LayerID, Vector


def make_main_layer(box: Optional[Box], origin: Optional[Vector] = None) -> StartLayer:
    return StartLayer(
        id=LayerID(id="%main%"), box=box, origin=origin or Vector(x=0, y=0)
    )


def make_layer(
    id_: str, box: Optional[Box], origin: Optional[Vector] = None
) -> StartLayer:
    return StartLayer(id=LayerID(id=id_), box=box, origin=origin or Vector(x=0, y=0))


def make_rectangle_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(
            Box.from_center_width_height((5, 5), 15, 10), origin=Vector(x=5, y=5)
        ),
        Shape.new_rectangle((5, 5), 2, 1, is_negative=False),
        EndLayer(),
    ]


def make_obround_horizontal_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(Box.from_center_width_height((0, 0), 5, 5)),
        Shape.new_obround((0, 1), 2, 1, is_negative=False),
        Shape.new_rectangle((0, -1), 2, 1, is_negative=False),
        EndLayer(),
    ]


def make_obround_vertical_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(Box.from_center_width_height((0, 0), 5, 5)),
        Shape.new_obround((-1, 0), 1, 2, is_negative=False),
        Shape.new_rectangle((1, 0), 1, 2, is_negative=False),
        EndLayer(),
    ]


def make_circle_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(
            Box.from_center_width_height((5, 5), 15, 10), origin=Vector(x=5, y=5)
        ),
        Shape.new_circle((5, 5), 2, is_negative=False),
        EndLayer(),
    ]


def make_circle_over_circle_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(Box.from_center_width_height((5, 5), 15, 10)),
        Shape.new_circle((5, 5), 2, is_negative=False),
        Shape.new_circle((5, 5), 1, is_negative=True),
        EndLayer(),
    ]


def make_paste_circle_over_circle_in_center_fixed_canvas() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer(box=Box.from_center_width_height((0, 0), 15, 10)) as layer:
        with layer.layer("D11") as d11:
            d11.circle((0, 0), 2, is_negative=False)
            d11.circle((0, 0), 1, is_negative=True)

        layer.paste(d11, (0, 0), is_negative=False)

    return builder.get_rvmc()


def make_paste_circle_over_paste_circle_in_center_dynamic_canvas() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        with layer.layer("D10") as d10:
            d10.circle((0, 0), 2, is_negative=False)
        with layer.layer("D11") as d11:
            d11.circle((0, 0), 1, is_negative=False)

        layer.paste(d10, (0, 0), is_negative=False)
        layer.paste(d11, (0, 0), is_negative=True)

    return builder.get_rvmc()


def make_paste_rectangle_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(Box.from_center_width_height((5, 5), 15, 10), Vector(x=5, y=5)),
        make_layer(
            "rect", Box.from_center_width_height((0, 0), 5, 5), Vector(x=0, y=0)
        ),
        Shape.new_rectangle((0, 0), 2, 1, is_negative=False),
        EndLayer(),
        Shape.new_rectangle((5, 5), 3, 2, is_negative=False),
        Shape.new_rectangle((5, 5), 2.8, 1.8, is_negative=True),
        PasteLayer.new("rect", (5, 5)),
        EndLayer(),
    ]


def make_paste_negative_rectangle_in_center_fixed_canvas() -> list[Command]:
    return [
        make_main_layer(Box.from_center_width_height((5, 5), 15, 10), Vector(x=5, y=5)),
        make_layer("rect", Box.from_center_width_height((0, 0), 5, 5)),
        Shape.new_rectangle((0, 0), 2, 1, is_negative=False),
        EndLayer(),
        Shape.new_rectangle((5, 5), 3, 2, is_negative=False),
        PasteLayer.new("rect", (5, 5), is_negative=True),
        EndLayer(),
    ]


def make_intersecting_rectangles_dynamic_canvas() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.rectangle((0, 0), 1, 2, is_negative=False)
        layer.rectangle((0, 0), 2, 1, is_negative=False)

    return builder.get_rvmc()


def make_intersecting_rectangles_2_dynamic_canvas() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.rectangle((0, 0), 1, 2, is_negative=False)
        layer.rectangle((0.5, 0.5), 2, 1, is_negative=False)

    return builder.get_rvmc()


def make_intersecting_rectangle_circle() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.rectangle((0, 0), 1, 4, is_negative=False)
        layer.circle((0.5, 0.5), 2, is_negative=False)

    return builder.get_rvmc()


def make_intersecting_circle_circle() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.circle((10, 10), 10, is_negative=False)
        layer.circle((5, 5), 10, is_negative=False)

    return builder.get_rvmc()


def make_intersecting_circle_circle_negative() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.circle((10, 10), 10, is_negative=False)
        layer.circle((5, 5), 10, is_negative=True)

    return builder.get_rvmc()


def make_intersecting_cross_0_0_circle_5_5() -> RVMC:
    builder = RvmcBuilder()
    with builder.layer() as layer:
        layer.cross((0, 0), 15, 20, 1, is_negative=False)
        layer.circle((5, 5), 5, is_negative=False)

    return builder.get_rvmc()
