from __future__ import annotations

from decimal import Decimal

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.state2 import State2
from pygerber.gerberx3.state_enums import (
    AxisCorrespondence,
    DrawMode,
    Mirroring,
    Polarity,
    Unit,
)
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID
from pygerber.gerberx3.tokenizer.tokens.coordinate import (
    Coordinate,
    CoordinateSign,
    CoordinateType,
)
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    AxisFormat,
    CoordinateParser,
)


def test_set_draw_units() -> None:
    state = State2()
    new_state = state.set_draw_units(Unit.Millimeters)
    assert new_state.get_draw_units() == Unit.Millimeters


def test_set_coordinate_parser() -> None:
    state = State2()
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    new_state = state.set_coordinate_parser(coordinate_parser)
    assert new_state.get_coordinate_parser() == coordinate_parser


def test_set_polarity() -> None:
    state = State2()
    new_state = state.set_polarity(Polarity.Dark)
    assert new_state.get_polarity() == Polarity.Dark


def test_set_mirroring() -> None:
    state = State2()
    new_state = state.set_mirroring(Mirroring.XY)
    assert new_state.get_mirroring() == Mirroring.XY


def test_set_rotation() -> None:
    state = State2()
    new_state = state.set_rotation(Decimal("90.0"))
    assert new_state.get_rotation() == Decimal("90.0")


def test_set_scaling() -> None:
    state = State2()
    scaling = Decimal(2)
    new_state = state.set_scaling(scaling)
    assert new_state.get_scaling() == scaling


def test_set_is_output_image_negation_required() -> None:
    state = State2()
    new_state = state.set_is_output_image_negation_required(value=True)
    assert new_state.get_is_output_image_negation_required() is True


def test_set_image_name() -> None:
    state = State2()
    new_state = state.set_image_name("image.png")
    assert new_state.get_image_name() == "image.png"


def test_set_file_name() -> None:
    state = State2()
    new_state = state.set_file_name("file.gbr")
    assert new_state.get_file_name() == "file.gbr"


def test_set_axis_correspondence() -> None:
    state = State2()
    new_state = state.set_axis_correspondence(AxisCorrespondence.AXBY)
    assert new_state.get_axis_correspondence() == AxisCorrespondence.AXBY


def test_set_draw_mode() -> None:
    state = State2()
    new_state = state.set_draw_mode(DrawMode.Linear)
    assert new_state.get_draw_mode() == DrawMode.Linear


def test_set_is_region() -> None:
    state = State2()
    new_state = state.set_is_region(is_region=True)
    assert new_state.get_is_region() is True


def test_set_is_aperture_block() -> None:
    state = State2()
    new_state = state.set_is_aperture_block(is_aperture_block=True)
    assert new_state.get_is_aperture_block() is True


def test_set_aperture_block_id() -> None:
    state = State2()
    new_state = state.set_aperture_block_id(ApertureID("D10"))
    assert new_state.get_aperture_block_id() == ApertureID("D10")


def test_set_is_step_and_repeat() -> None:
    state = State2()
    new_state = state.set_is_step_and_repeat(True)
    assert new_state.get_is_step_and_repeat() is True


def test_set_is_multi_quadrant() -> None:
    state = State2()
    new_state = state.set_is_multi_quadrant(is_multi_quadrant=True)
    assert new_state.get_is_multi_quadrant() is True


def test_set_current_position() -> None:
    state = State2()
    v = Vector2D.new(10, 10)
    new_state = state.set_current_position(v)
    assert new_state.get_current_position() == v


def test_set_current_aperture_id() -> None:
    state = State2()
    new_state = state.set_current_aperture_id(ApertureID("D10"))
    assert new_state.get_current_aperture_id() == ApertureID("D10")


def test_parse_coordinate() -> None:
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    c = Coordinate(
        coordinate_type=CoordinateType.X,
        sign=CoordinateSign.Positive,
        offset="0001000000",
    )
    state = (
        State2()
        .set_coordinate_parser(coordinate_parser)
        .set_draw_units(Unit.Millimeters)
    )
    offset = state.parse_coordinate(c)
    assert offset == Offset.new(1)
