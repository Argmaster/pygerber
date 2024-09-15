from __future__ import annotations

from typing import Optional

from pygerber.vm import Builder
from pygerber.vm.commands import EndLayer, PasteLayer, Shape, StartLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector


def test_circle() -> None:
    assert build_circle() == RVMC(
        commands=[
            default_start_main_layer(),
            Shape.new_circle(center=(0.0, 0.0), diameter=1.0, is_negative=False),
            default_end_layer(),
        ]
    )


def build_circle() -> RVMC:
    builder = Builder()

    with builder.layer() as layer:
        layer.circle((0, 0), 1, is_negative=False)

    return builder.commands


def default_start_main_layer(origin: Optional[Vector] = None) -> StartLayer:
    return StartLayer(
        id=LayerID(id="%main%"), box=None, origin=origin or Vector(x=0.0, y=0.0)
    )


def default_start_layer(
    id_: str = "D10", origin: Optional[Vector] = None
) -> StartLayer:
    return StartLayer(
        id=LayerID(id=id_), box=None, origin=origin or Vector(x=0.0, y=0.0)
    )


def default_end_layer() -> EndLayer:
    return EndLayer()


def test_nested_layer_circle_paste() -> None:
    assert build_nested_layer_circle_paste() == RVMC(
        commands=[
            default_start_main_layer(),
            default_start_layer("D10"),
            Shape.new_circle(center=(0.0, 0.0), diameter=1.0, is_negative=False),
            default_end_layer(),
            PasteLayer(
                source_layer_id=LayerID(id="D10"),
                center=Vector(x=0.0, y=0.0),
                is_negative=False,
            ),
            default_end_layer(),
        ]
    )


def build_nested_layer_circle_paste() -> RVMC:
    builder = Builder()

    with builder.layer() as layer:
        with layer.layer("D10") as d10:
            d10.circle((0, 0), 1, is_negative=False)
        layer.paste(d10, (0, 0), is_negative=False)

    return builder.commands


def build_nested_layer_circle_paste_with_offset() -> RVMC:
    builder = Builder()

    with builder.layer() as layer:
        with layer.layer("D10") as d10:
            d10.circle((0, 0), 1, is_negative=False)
        layer.paste(d10, (5, 5), is_negative=False)

    return builder.commands


def test_nested_layer_circle_paste_with_offset() -> None:
    assert build_nested_layer_circle_paste_with_offset() == RVMC(
        commands=[
            default_start_main_layer(),
            default_start_layer("D10"),
            Shape.new_circle(center=(0.0, 0.0), diameter=1.0, is_negative=False),
            default_end_layer(),
            PasteLayer(
                source_layer_id=LayerID(id="D10"),
                center=Vector(x=5.0, y=5.0),
                is_negative=False,
            ),
            default_end_layer(),
        ]
    )


def build_main_origin_x_y_layer_origin_x_y_paste_x_y(
    main_origin: tuple[float, float],
    layer_origin: tuple[float, float],
    paste: tuple[float, float],
    circle_at: tuple[float, float] = (0, 0),
) -> RVMC:
    builder = Builder()

    with builder.layer(origin=main_origin) as layer:
        with layer.layer("D10", origin=layer_origin) as d10:
            d10.circle(circle_at, 1, is_negative=False)
        layer.paste(d10, paste, is_negative=False)
        layer.cross((0, 0), 9, 9, 0.05, is_negative=False)
        layer.x(main_origin, 1, 0.05, is_negative=False)

    return builder.commands


def build_main_origin_x_y_layer_origin_x_y_paste_x_y_no_main_origin_mark(
    main_origin: tuple[float, float],
    layer_origin: tuple[float, float],
    paste: tuple[float, float],
    circle_at: tuple[float, float] = (0, 0),
) -> RVMC:
    builder = Builder()

    with builder.layer(origin=main_origin) as layer:
        with layer.layer("D10", origin=layer_origin) as d10:
            d10.circle(circle_at, 1, is_negative=False)
        layer.paste(d10, paste, is_negative=False)
        layer.cross((0, 0), 9, 9, 0.05, is_negative=False)

    return builder.commands
