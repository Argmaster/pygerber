from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from test.gerberx3.test_parser2.common import debug_dump_context, parse_code
from unittest.mock import MagicMock

import pytest

from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser.errors import (
    IncrementalCoordinatesNotSupportedError,
    ZeroOmissionNotSupportedError,
)
from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotDefined2Error,
    NestedRegionNotAllowedError,
    NoValidArcCenterFoundError,
    OnUpdateDrawingState2Error,
    ReferencedNotInitializedBlockBufferError,
    UnnamedBlockApertureNotAllowedError,
)
from pygerber.gerberx3.state_enums import AxisCorrespondence, DrawMode, Polarity, Unit
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    AxisFormat,
    CoordinateParser,
)

DEBUG_DUMP_DIR = Path(__file__).parent / ".output" / "test_parser2hooks"
DEBUG_DUMP_DIR.mkdir(exist_ok=True, parents=True)


def test_begin_block_aperture_token_hooks() -> None:
    gerber_source = "%ABD10*%"

    context = Parser2Context()
    context.set_is_aperture_block(is_aperture_block=False)
    context.set_aperture_block_id(None)

    parse_code(gerber_source, context)

    assert context.get_is_aperture_block() is True
    assert context.get_aperture_block_id() == "D10"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_begin_block_aperture_token_hooks.__qualname__,
    )


def test_begin_block_aperture_token_hooks_nested_region() -> None:
    gerber_source = "%ABD10*%%ABD11*%"

    context = Parser2Context()

    with pytest.raises(NestedRegionNotAllowedError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_begin_block_aperture_token_hooks.__qualname__,
    )


def test_end_block_aperture_token_hooks_uninitialized_block() -> None:
    gerber_source = "%AB*%"

    context = Parser2Context()

    with pytest.raises(ReferencedNotInitializedBlockBufferError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_end_block_aperture_token_hooks_uninitialized_block.__qualname__,
    )


def test_end_block_aperture_token_hooks_unnamed_block() -> None:
    gerber_source = "%AB*%"

    context = Parser2Context()
    context.push_block_command_buffer()

    with pytest.raises(UnnamedBlockApertureNotAllowedError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_end_block_aperture_token_hooks_unnamed_block.__qualname__,
    )


def test_end_block_aperture_token_hooks() -> None:
    gerber_source = "%AB*%"

    context = Parser2Context()
    context.push_block_command_buffer()
    context.set_is_aperture_block(is_aperture_block=True)
    context.set_aperture_block_id(ApertureID("D10"))

    parse_code(gerber_source, context)

    assert context.get_is_aperture_block() is False
    assert context.get_aperture_block_id() is None

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_end_block_aperture_token_hooks.__qualname__,
    )


def test_define_aperture_circle_token_hooks() -> None:
    gerber_source = "%ADD20C,1.778000*%"
    unit = Unit.Millimeters
    expected_diameter = Offset.new(value=Decimal("1.778000"), unit=unit)
    expected_hole_diameter = None

    context = Parser2Context()
    context.set_draw_units(unit)
    parse_code(gerber_source, context)

    aperture = context.get_aperture(ApertureID("D20"))
    assert isinstance(aperture, Circle2)
    assert aperture.diameter == expected_diameter
    assert aperture.hole_diameter == expected_hole_diameter

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_define_aperture_circle_token_hooks.__qualname__,
    )


def test_define_aperture_rectangle_token_hooks() -> None:
    gerber_source = "%ADD17R,0.500000X0.550000*%"
    unit = Unit.Millimeters
    expected_x_size = Offset.new(value=Decimal("0.500000"), unit=unit)
    expected_y_size = Offset.new(value=Decimal("0.550000"), unit=unit)
    expected_hole_diameter = None

    context = Parser2Context()
    context.set_draw_units(unit)
    parse_code(gerber_source, context)

    aperture = context.get_aperture(ApertureID("D17"))
    assert isinstance(aperture, Rectangle2)
    assert aperture.x_size == expected_x_size
    assert aperture.y_size == expected_y_size
    assert aperture.hole_diameter == expected_hole_diameter

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_define_aperture_rectangle_token_hooks.__qualname__,
    )


def test_define_aperture_obround_token_hooks() -> None:
    gerber_source = "%ADD17O,0.500000X0.550000*%"
    unit = Unit.Millimeters
    expected_x_size = Offset.new(value=Decimal("0.500000"), unit=unit)
    expected_y_size = Offset.new(value=Decimal("0.550000"), unit=unit)
    expected_hole_diameter = None

    context = Parser2Context()
    context.set_draw_units(unit)
    parse_code(gerber_source, context)

    aperture = context.get_aperture(ApertureID("D17"))
    assert isinstance(aperture, Obround2)
    assert aperture.x_size == expected_x_size
    assert aperture.y_size == expected_y_size
    assert aperture.hole_diameter == expected_hole_diameter

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_define_aperture_obround_token_hooks.__qualname__,
    )


def test_define_aperture_polygon_token_hooks() -> None:
    gerber_source = "%ADD17P,0.6X5X90X0.3*%"
    unit = Unit.Millimeters
    expected_outer_diameter = Offset.new(value=Decimal("0.600000"), unit=unit)
    expected_number_vertices = 5
    expected_rotation = Decimal("90")
    expected_hole_diameter = Offset.new(value=Decimal("0.300000"), unit=unit)

    context = Parser2Context()
    context.set_draw_units(unit)
    parse_code(gerber_source, context)

    aperture = context.get_aperture(ApertureID("D17"))
    assert isinstance(aperture, Polygon2)
    assert aperture.outer_diameter == expected_outer_diameter
    assert aperture.number_vertices == expected_number_vertices
    assert aperture.rotation == expected_rotation
    assert aperture.hole_diameter == expected_hole_diameter

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_define_aperture_polygon_token_hooks.__qualname__,
    )


def test_define_aperture_macro_token_hooks() -> None:
    gerber_source = """
    %AMDonut*
    1,1,$1,$2,$3*
    $4=$1x0.75*
    1,0,$4,$2,$3*
    %
    %ADD17Donut,0.30X0X0*%
    """
    unit = Unit.Millimeters

    context = Parser2Context()
    context.set_draw_units(unit)
    parse_code(gerber_source, context)

    aperture = context.get_aperture(ApertureID("D17"))
    assert isinstance(aperture, Macro2)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_define_aperture_polygon_token_hooks.__qualname__,
    )


def test_axis_select_token_hooks_token_hooks() -> None:
    gerber_source = "%ASAYBX*%"

    context = Parser2Context()
    assert context.get_axis_correspondence() == AxisCorrespondence.AXBY

    parse_code(gerber_source, context)

    assert context.get_axis_correspondence() == AxisCorrespondence.AYBX

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_axis_select_token_hooks_token_hooks.__qualname__,
    )


def test_command_draw_line_token_hooks() -> None:
    gerber_source = """
    X151892000Y-57658000D01*
    """
    unit = Unit.Millimeters
    draw_mode = DrawMode.Linear
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    end_point = Vector2D(x=Offset.new("151.892000"), y=Offset.new("-57.6580000"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_aperture(current_aperture, aperture_mock)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 1
    assert next(iter(cmd)) == Line2(
        attributes=ImmutableMapping[str, str](),
        polarity=polarity,
        aperture_id=current_aperture,
        start_point=Vector2D(x=Offset.new("0"), y=Offset.new("0")),
        end_point=end_point,
    )
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_draw_arc_token_hooks_multi_quadrant() -> None:
    gerber_source = """
    X156019500Y-66357500I466639J-1274902D01*
    """
    unit = Unit.Millimeters
    is_multi_quadrant = True
    draw_mode = DrawMode.ClockwiseCircular
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("156.019500"), y=Offset.new("156.019500"))
    center_point = Vector2D(x=Offset.new("156.486139"), y=Offset.new("154.744598"))
    end_point = Vector2D(x=Offset.new("156.019500"), y=Offset.new("-66.357500"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture, aperture_mock)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 1
    assert next(iter(cmd)) == Arc2(
        attributes=ImmutableMapping[str, str](),
        polarity=polarity,
        aperture_id=current_aperture,
        start_point=start_point,
        center_point=center_point,
        end_point=end_point,
    )
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_draw_arc_token_hooks_single_quadrant() -> None:
    gerber_source = """
    X060000Y000000I000000J060000D01*
    """
    unit = Unit.Millimeters
    is_multi_quadrant = False
    draw_mode = DrawMode.ClockwiseCircular
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=2, decimal=4),
        y_format=AxisFormat(integer=2, decimal=4),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    center_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("0.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("0.0"))
    expected_angle = 90.0

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture, aperture_mock)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 1
    assert next(iter(cmd)) == Arc2(
        attributes=ImmutableMapping[str, str](),
        polarity=polarity,
        aperture_id=current_aperture,
        start_point=start_point,
        center_point=center_point,
        end_point=end_point,
    )
    assert context.get_current_position() == end_point
    assert start_point.angle_between(end_point) == expected_angle

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_draw_arc_token_hooks_single_quadrant_135_degrees() -> None:
    gerber_source = """
    X042426Y-042426I000000J060000D01*
    """
    unit = Unit.Millimeters
    is_multi_quadrant = False
    draw_mode = DrawMode.ClockwiseCircular
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=2, decimal=4),
        y_format=AxisFormat(integer=2, decimal=4),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture, aperture_mock)

    with pytest.raises(NoValidArcCenterFoundError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_draw_arc_token_hooks_single_quadrant_45_degrees() -> None:
    gerber_source = """
    X042426Y042426I000000J060000D01*
    """
    unit = Unit.Millimeters
    is_multi_quadrant = False
    draw_mode = DrawMode.ClockwiseCircular
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=2, decimal=4),
        y_format=AxisFormat(integer=2, decimal=4),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    center_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("0.0"))
    end_point = Vector2D(x=Offset.new("4.2426"), y=Offset.new("4.2426"))
    expected_angle = 45.0

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture, aperture_mock)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 1
    assert next(iter(cmd)) == Arc2(
        attributes=ImmutableMapping[str, str](),
        polarity=polarity,
        aperture_id=current_aperture,
        start_point=start_point,
        center_point=center_point,
        end_point=end_point,
    )
    assert context.get_current_position() == end_point
    assert start_point.angle_between(end_point) == expected_angle

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_move_token_hooks() -> None:
    gerber_source = """
    X0006000000Y0006000000D02*
    """
    unit = Unit.Millimeters
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("0.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("6.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_coordinate_parser(coordinate_parser)
    context.set_current_position(start_point)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 0
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_flash_token_hooks() -> None:
    gerber_source = """
    X0006000000Y0006000000D03*
    """
    unit = Unit.Millimeters
    draw_mode = DrawMode.Linear
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=4, decimal=6),
        y_format=AxisFormat(integer=4, decimal=6),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("0.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("6.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture)
    context.set_aperture(current_aperture, aperture_mock)
    context.set_current_position(start_point)

    parse_code(gerber_source, context)
    cmd = context.main_command_buffer.get_readonly()

    assert len(cmd) == 1
    assert next(iter(cmd)) == Flash2(
        attributes=ImmutableMapping[str, str](),
        polarity=polarity,
        aperture_id=current_aperture,
        flash_point=end_point,
    )
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_select_aperture_token_hooks_not_defined() -> None:
    gerber_source = """
    D20*
    """
    unit = Unit.Millimeters

    context = Parser2Context()
    context.set_draw_units(unit)

    with pytest.raises(ApertureNotDefined2Error):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_select_aperture_token_hooks_not_defined.__qualname__,
    )


def test_select_aperture_token_hooks() -> None:
    gerber_source = """
    %ADD20C,1.778000*%
    D20*
    """
    unit = Unit.Millimeters

    context = Parser2Context()
    context.set_draw_units(unit)

    parse_code(gerber_source, context)

    assert context.get_current_aperture_id() == ApertureID("D20")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_select_aperture_token_hooks.__qualname__,
    )


def test_coordinate_format_token_hooks_absolute_leading() -> None:
    gerber_source = "%FSLAX24Y24*%"

    context = Parser2Context()
    parse_code(gerber_source, context)

    coordinate_parser = context.get_coordinate_parser()
    assert coordinate_parser.x_format == AxisFormat(integer=2, decimal=4)
    assert coordinate_parser.y_format == AxisFormat(integer=2, decimal=4)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_coordinate_format_token_hooks_absolute_leading.__qualname__,
    )


def test_coordinate_format_token_hooks_incremental_leading() -> None:
    gerber_source = """
    %FSLIX24Y24*%
    """

    context = Parser2Context()
    try:
        parse_code(gerber_source, context)
    except OnUpdateDrawingState2Error as e:
        assert isinstance(  # noqa: PT017
            e.__cause__,
            IncrementalCoordinatesNotSupportedError,
        )
    else:
        pytest.fail("Not raised OnUpdateDrawingState2Error")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_coordinate_format_token_hooks_absolute_leading.__qualname__,
    )


def test_coordinate_format_token_hooks_incremental_trailing() -> None:
    gerber_source = """
    %FSTAX24Y24*%
    """

    context = Parser2Context()
    try:
        parse_code(gerber_source, context)
    except OnUpdateDrawingState2Error as e:
        assert isinstance(  # noqa: PT017
            e.__cause__,
            ZeroOmissionNotSupportedError,
        )
    else:
        pytest.fail("Not raised OnUpdateDrawingState2Error")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_coordinate_format_token_hooks_absolute_leading.__qualname__,
    )


def test_set_linear_token_hooks() -> None:
    gerber_source = """
    G01*
    """

    context = Parser2Context()
    context.set_draw_mode(DrawMode.ClockwiseCircular)

    parse_code(gerber_source, context)

    assert context.get_draw_mode() is DrawMode.Linear

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_linear_token_hooks.__qualname__,
    )


def test_set_clockwise_circular_token_hooks() -> None:
    gerber_source = """
    G02*
    """

    context = Parser2Context()
    context.set_draw_mode(DrawMode.Linear)

    parse_code(gerber_source, context)

    assert context.get_draw_mode() is DrawMode.ClockwiseCircular

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_clockwise_circular_token_hooks.__qualname__,
    )


def test_set_counterclockwise_circular_token_hooks() -> None:
    gerber_source = """
    G03*
    """

    context = Parser2Context()
    context.set_draw_mode(DrawMode.Linear)

    parse_code(gerber_source, context)

    assert context.get_draw_mode() is DrawMode.CounterclockwiseCircular

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_counterclockwise_circular_token_hooks.__qualname__,
    )
