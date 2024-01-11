from __future__ import annotations

import datetime
from decimal import Decimal
from pathlib import Path
from test.gerberx3.test_parser2.common import debug_dump_context, parse_code
from unittest.mock import MagicMock

import pytest

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
from pygerber.gerberx3.parser2.attributes2 import (
    AperFunctionAttribute,
    ObjectAttributes,
)
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2
from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotDefined2Error,
    NestedRegionNotAllowedError,
    NoValidArcCenterFoundError,
    OnUpdateDrawingState2Error,
    ReferencedNotInitializedBlockBufferError,
    RegionNotInitializedError,
    StepAndRepeatNotInitializedError,
    UnitNotSet2Error,
    UnnamedBlockApertureNotAllowedError,
)
from pygerber.gerberx3.state_enums import (
    AxisCorrespondence,
    DrawMode,
    Mirroring,
    Polarity,
    Unit,
)
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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Line2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.start_point == Vector2D(x=Offset.new("0"), y=Offset.new("0"))
    assert cmd.end_point == end_point
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_command_draw_line_token_hooks_6() -> None:
    gerber_source = """
    X060000Y000000I000000J060000D01*
    """
    unit = Unit.Millimeters
    is_multi_quadrant = False
    draw_mode = DrawMode.Linear
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=2, decimal=4),
        y_format=AxisFormat(integer=2, decimal=4),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("0.0"))

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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Line2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.start_point == start_point
    assert cmd.end_point == end_point
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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.start_point == start_point
    assert cmd.center_point == center_point
    assert cmd.end_point == end_point
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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.start_point == start_point
    assert cmd.center_point == center_point
    assert cmd.end_point == end_point
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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.start_point == start_point
    assert cmd.center_point == center_point
    assert cmd.end_point == end_point
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
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Flash2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.polarity == polarity
    assert cmd.aperture_id == current_aperture
    assert cmd.flash_point == end_point
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
        / test_coordinate_format_token_hooks_incremental_leading.__qualname__,
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
        / test_coordinate_format_token_hooks_incremental_trailing.__qualname__,
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


def test_begin_region_token_hooks() -> None:
    gerber_source = """
    G36*
    """

    context = Parser2Context()
    context.set_is_region(is_region=False)

    parse_code(gerber_source, context)
    assert context.get_is_region() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_begin_region_token_hooks.__qualname__,
    )


def test_end_region_token_hooks_fail_without_g36() -> None:
    gerber_source = """
    G37*
    """

    context = Parser2Context()
    context.set_is_region(is_region=True)

    with pytest.raises(RegionNotInitializedError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_end_region_token_hooks_fail_without_g36.__qualname__,
    )


def test_end_region_token_hooks() -> None:
    gerber_source = """
    G36*
    G37*
    """

    context = Parser2Context()
    context.set_is_region(is_region=True)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert context.get_is_region() is False

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Region2)
    assert len(cmd.command_buffer) == 0

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_end_region_token_hooks.__qualname__,
    )


def test_set_unit_inches_token_hooks() -> None:
    gerber_source = """
    G70*
    """

    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    assert context.get_draw_units() is Unit.Inches

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_unit_inches_token_hooks.__qualname__,
    )


def test_set_unit_mm_token_hooks() -> None:
    gerber_source = """
    G71*
    """

    context = Parser2Context()
    context.set_draw_units(Unit.Inches)

    parse_code(gerber_source, context)

    assert context.get_draw_units() is Unit.Millimeters

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_unit_mm_token_hooks.__qualname__,
    )


def test_set_single_quadrant_mode() -> None:
    gerber_source = """
    G74*
    """

    context = Parser2Context()
    context.set_is_multi_quadrant(is_multi_quadrant=True)

    parse_code(gerber_source, context)

    assert context.get_is_multi_quadrant() is False

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_unit_mm_token_hooks.__qualname__,
    )


def test_set_multi_quadrant_mode() -> None:
    gerber_source = """
    G75*
    """

    context = Parser2Context()
    context.set_is_multi_quadrant(is_multi_quadrant=False)

    parse_code(gerber_source, context)

    assert context.get_is_multi_quadrant() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_unit_mm_token_hooks.__qualname__,
    )


@pytest.mark.skip(reason="G90 not properly implemented.")
def test_set_coordinate_absolute_token_hooks() -> None:
    gerber_source = """
    G90*
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_coordinate_absolute_token_hooks.__qualname__,
    )


@pytest.mark.skip(reason="G91 not properly implemented.")
def test_set_coordinate_relative_token_hooks() -> None:
    gerber_source = """
    G91*
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_set_coordinate_relative_token_hooks.__qualname__,
    )


def test_image_name_token_hooks() -> None:
    gerber_source = """
    %INfoobar*%
    """

    context = Parser2Context()
    assert context.get_image_name() is None

    parse_code(gerber_source, context)

    assert context.get_image_name() == "foobar"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_image_name_token_hooks.__qualname__,
    )


def test_image_polarity_token_hooks() -> None:
    gerber_source = """
    %IPNEG*%
    """

    context = Parser2Context()
    assert context.get_is_output_image_negation_required() is False

    parse_code(gerber_source, context)

    assert context.get_is_output_image_negation_required() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_image_polarity_token_hooks.__qualname__,
    )


def test_load_mirror_token_hooks() -> None:
    gerber_source = """
    %LMX*%
    """

    context = Parser2Context()
    assert context.get_mirroring() is Mirroring.NoMirroring

    parse_code(gerber_source, context)

    assert context.get_mirroring() is Mirroring.X

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_load_mirror_token_hooks.__qualname__,
    )


def test_load_name_token_hooks() -> None:
    gerber_source = """
    %LNfoobar*%
    """

    context = Parser2Context()
    assert context.get_file_name() is None

    parse_code(gerber_source, context)

    assert context.get_file_name() == "foobar"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_load_name_token_hooks.__qualname__,
    )


def test_load_rotation_token_hooks() -> None:
    gerber_source = """
    %LR45*%
    """

    context = Parser2Context()
    assert context.get_rotation() == Decimal("0")

    parse_code(gerber_source, context)

    assert context.get_rotation() == Decimal("45")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_load_name_token_hooks.__qualname__,
    )


def test_load_scaling_token_hooks() -> None:
    gerber_source = """
    %LS2*%
    """

    context = Parser2Context()
    assert context.get_scaling() == Decimal("1")

    parse_code(gerber_source, context)

    assert context.get_scaling() == Decimal("2")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_load_scaling_token_hooks.__qualname__,
    )


def test_program_stop_token_hooks_no_commands() -> None:
    gerber_source = """M00*"""

    context = Parser2Context()
    assert context.get_reached_program_stop() is False

    parse_code(gerber_source, context)

    assert context.get_reached_program_stop() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_program_stop_token_hooks_no_commands.__qualname__,
    )


def test_optional_stop_token_hook_stop_commands() -> None:
    gerber_source = """M01*"""

    context = Parser2Context()
    assert context.get_reached_optional_stop() is False

    parse_code(gerber_source, context)

    assert context.get_reached_optional_stop() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_optional_stop_token_hook_stop_commands.__qualname__,
    )


def test_end_of_file_token_hooks() -> None:
    gerber_source = "M02*"

    context = Parser2Context()
    assert context.get_reached_end_of_file() is False

    parse_code(gerber_source, context)

    assert context.get_reached_end_of_file() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_end_of_file_token_hooks.__qualname__,
    )


def test_unit_mode_token_hooks_inch() -> None:
    gerber_source = """
    %MOIN*%
    """

    context = Parser2Context()
    with pytest.raises(UnitNotSet2Error):
        context.get_draw_units()

    parse_code(gerber_source, context)

    assert context.get_draw_units() is Unit.Inches

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_unit_mode_token_hooks_inch.__qualname__,
    )


def test_unit_mode_token_hooks_mm() -> None:
    gerber_source = """
        %MOMM*%
        """

    context = Parser2Context()
    with pytest.raises(UnitNotSet2Error):
        context.get_draw_units()

    parse_code(gerber_source, context)

    assert context.get_draw_units() is Unit.Millimeters

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_unit_mode_token_hooks_mm.__qualname__,
    )


def test_step_and_repeat_token_hooks() -> None:
    gerber_source = """
    %SRX3Y2I5.0J4.0*%
    """

    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    assert context.get_is_step_and_repeat() is True

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_step_and_repeat_token_hooks.__qualname__,
    )


def test_step_and_repeat_token_hooks_fail_uninitialized_sr() -> None:
    gerber_source = """
    %SR*%
    """

    context = Parser2Context()

    with pytest.raises(StepAndRepeatNotInitializedError):
        parse_code(gerber_source, context)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_step_and_repeat_token_hooks.__qualname__,
    )


def test_step_and_repeat_token_hooks_with_lines() -> None:
    x_repeats = 3
    y_repeats = 2
    step_x = Offset.new("1.0")
    step_y = Offset.new("2.0")

    gerber_source = f"""
    %SRX{x_repeats}Y{y_repeats}I{step_x.value:.1f}J{step_y.value:.1f}*%
    D11*
    X060000Y000000I000000J060000D01*
    %SR*%
    """
    unit = Unit.Millimeters
    is_multi_quadrant = False
    draw_mode = DrawMode.Linear
    coordinate_parser = CoordinateParser.new(
        x_format=AxisFormat(integer=2, decimal=4),
        y_format=AxisFormat(integer=2, decimal=4),
    )
    polarity = Polarity.Dark
    current_aperture = ApertureID("D11")
    aperture_mock = MagicMock()
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("0.0"))
    expected_command_count = 6

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
    main_cmd_buffer = context.main_command_buffer.get_readonly()

    assert len(main_cmd_buffer) == expected_command_count

    i = 0

    for xi in range(x_repeats):
        for yi in range(y_repeats):
            sr_cmd_buffer = main_cmd_buffer[i]
            offset = Vector2D(
                x=step_x * xi,
                y=step_y * yi,
            )

            assert isinstance(sr_cmd_buffer, BufferCommand2)
            assert len(sr_cmd_buffer.command_buffer) == 1

            for cmd in sr_cmd_buffer:
                assert isinstance(cmd, Line2)
                assert cmd.attributes == ObjectAttributes()
                assert cmd.polarity == polarity
                assert cmd.aperture_id == current_aperture
                assert cmd.start_point == start_point + offset
                assert cmd.end_point == end_point + offset

            i += 1

    assert context.get_is_step_and_repeat() is False

    with pytest.raises(StepAndRepeatNotInitializedError):
        context.get_step_and_repeat_command_buffer()

    with pytest.raises(StepAndRepeatNotInitializedError):
        context.get_state_before_step_and_repeat()

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


def test_aperture_attribute_token_hooks_AperFunction_EtchedComponent() -> None:
    gerber_source = """
    %TA.AperFunction,EtchedComponent*%
    """

    context = Parser2Context()

    parse_code(gerber_source, context)

    aper_function = context.aperture_attributes.AperFunction
    assert aper_function is not None
    assert aper_function.function == AperFunctionAttribute.Function.EtchedComponent
    assert aper_function.field == ""

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_aperture_attribute_token_hooks_AperFunction_EtchedComponent.__qualname__,
    )


def test_aperture_attribute_token_hooks_AperFunction_SMDPad() -> None:
    gerber_source = """
    %TA.AperFunction,SMDPad,CuDef*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    aper_function = context.aperture_attributes.AperFunction
    assert aper_function is not None
    assert aper_function.function == AperFunctionAttribute.Function.SMDPad
    assert aper_function.field == "CuDef"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_aperture_attribute_token_hooks_AperFunction_SMDPad.__qualname__,
    )


def test_object_attributes_token_hooks_N() -> None:
    gerber_source = r"""
    %TO.N,/NAND Flash \002C eMMC\002C T-Card and Audio/NAND0-ALE\005CSDC2-DS*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    name = context.object_attributes.N
    assert name is not None
    assert name == r"/NAND Flash \002C eMMC\002C T-Card and Audio/NAND0-ALE\005CSDC2-DS"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_N.__qualname__,
    )


def test_object_attributes_token_hooks_P() -> None:
    gerber_source = r"""
    %TO.P,LAN1,10*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    pin = context.object_attributes.P
    assert pin is not None
    assert pin.refdes == "LAN1"
    assert pin.number == "10"
    assert pin.function is None

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_P.__qualname__,
    )


def test_object_attributes_token_hooks_C() -> None:
    gerber_source = r"""
    %TO.C,C123*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    attribute_c = context.object_attributes.C
    assert attribute_c is not None
    assert attribute_c == "C123"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_C.__qualname__,
    )


def test_object_attributes_token_hooks_update_C() -> None:
    gerber_source = r"""
    %TO.C,C123*%
    %TO.C,FID4*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    attribute_c = context.object_attributes.C
    assert attribute_c is not None
    assert attribute_c == "FID4"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_C.__qualname__,
    )


def test_file_attributes_token_hooks() -> None:
    gerber_source = r"""
    %TF.GenerationSoftware,KiCad,Pcbnew,5.1.5-52549c5~84~ubuntu18.04.1*%
    %TF.CreationDate,2020-02-11T15:54:30+02:00*%
    %TF.ProjectId,A64-OlinuXino_Rev_G,4136342d-4f6c-4696-9e75-58696e6f5f52,G*%
    %TF.SameCoordinates,Original*%
    %TF.FileFunction,Soldermask,Bot*%
    %TF.FilePolarity,Negative*%
    """

    context = Parser2Context()
    parse_code(gerber_source, context)

    gs = context.file_attributes.GenerationSoftware
    assert gs is not None
    assert gs.name == "KiCad"
    assert gs.guid == "Pcbnew"
    assert gs.revision == "5.1.5-52549c5~84~ubuntu18.04.1"

    assert context.file_attributes.CreationDate == datetime.datetime.fromisoformat(
        "2020-02-11T15:54:30+02:00",
    )
    assert (
        context.file_attributes.ProjectId
        == "A64-OlinuXino_Rev_G,4136342d-4f6c-4696-9e75-58696e6f5f52,G"
    )
    assert context.file_attributes.SameCoordinates == "Original"
    assert context.file_attributes.FileFunction == "Soldermask,Bot"
    assert context.file_attributes.FilePolarity == "Negative"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_file_attributes_token_hooks.__qualname__,
    )


def test_delete_attribute_token_hooks_C() -> None:
    gerber_source = r"""
    %TO.C,C123*%
    %TO.P,LAN1,10*%
    %TD.C*%
    """

    context = Parser2Context()
    context.set_object_attribute("C", "C123")
    parse_code(gerber_source, context)

    attribute_c = context.object_attributes.C
    assert attribute_c is None

    pin = context.object_attributes.P
    assert pin is not None
    assert pin.refdes == "LAN1"
    assert pin.number == "10"
    assert pin.function is None

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_C.__qualname__,
    )


def test_delete_attribute_token_hooks_all() -> None:
    gerber_source = r"""
    %TF.GenerationSoftware,KiCad,Pcbnew,5.1.5-52549c5~84~ubuntu18.04.1*%
    %TO.C,C123*%
    %TO.P,LAN1,10*%
    %TD*%
    """

    context = Parser2Context()
    context.set_object_attribute("C", "C123")
    parse_code(gerber_source, context)

    attribute_c = context.object_attributes.C
    assert attribute_c is None

    pin = context.object_attributes.P
    assert pin is None

    gen_sw = context.file_attributes.GenerationSoftware

    assert gen_sw is not None
    assert gen_sw.name == "KiCad"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_object_attributes_token_hooks_C.__qualname__,
    )
