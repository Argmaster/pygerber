from __future__ import annotations

import datetime
from decimal import Decimal
from pathlib import Path

import pytest

from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
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
    IncrementalCoordinatesNotSupported2Error,
    NoValidArcCenterFoundError,
    OnUpdateDrawingState2Error,
    ReferencedNotInitializedBlockBufferError,
    RegionNotInitializedError,
    StepAndRepeatNotInitializedError,
    UnitNotSet2Error,
    UnnamedBlockApertureNotAllowedError,
    ZeroOmissionNotSupported2Error,
)
from pygerber.gerberx3.parser2.macro2.assignment2 import Assignment2
from pygerber.gerberx3.parser2.macro2.expressions2.binary2 import (
    Addition2,
    Multiplication2,
    Subtraction2,
)
from pygerber.gerberx3.parser2.macro2.expressions2.constant2 import Constant2
from pygerber.gerberx3.parser2.macro2.expressions2.unary2 import Negation2
from pygerber.gerberx3.parser2.macro2.expressions2.variable_name import VariableName2
from pygerber.gerberx3.parser2.macro2.primitives2.code_1_circle2 import Code1Circle2
from pygerber.gerberx3.parser2.macro2.primitives2.code_4_outline2 import Code4Outline2
from pygerber.gerberx3.parser2.macro2.primitives2.code_5_polygon2 import Code5Polygon2
from pygerber.gerberx3.parser2.macro2.primitives2.code_7_thermal2 import Code7Thermal2
from pygerber.gerberx3.parser2.macro2.primitives2.code_20_vector_line2 import (
    Code20VectorLine2,
)
from pygerber.gerberx3.parser2.macro2.primitives2.code_21_center_line2 import (
    Code21CenterLine2,
)
from pygerber.gerberx3.parser2.state2 import ApertureTransform
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
from test.gerberx3.test_parser2.common import debug_dump_context, parse_code

DEBUG_DUMP_DIR = Path(__file__).parent / ".output" / "test_parser2hooks"
DEBUG_DUMP_DIR.mkdir(exist_ok=True, parents=True)


def test_macro_definition_token_hooks_one_circle() -> None:
    gerber_source = """
    %AMCircle*
    1,1,1.5,0,0,0*%
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Circle")

    assert macro.name == "Circle"
    assert len(macro.statements) == 1

    c = macro.statements[0]

    assert isinstance(c, Code1Circle2)

    assert isinstance(c.diameter, Constant2)
    assert c.diameter.value == Offset.new("1.5")

    assert isinstance(c.center_x, Constant2)
    assert c.center_x.value == Offset.new("0")

    assert isinstance(c.center_y, Constant2)
    assert c.center_y.value == Offset.new("0")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_one_code_4_outline() -> None:
    gerber_source = """
    %AMTriangle_30*
    4,1,3,
    1,-1,
    1,1,
    2,1,
    1,-1,
    30*%
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Triangle_30")
    assert macro.name == "Triangle_30"

    assert len(macro.statements) == 1

    outline = macro.statements[0]
    assert isinstance(outline, Code4Outline2)
    assert isinstance(outline.exposure, Constant2)
    assert outline.exposure.value == Offset.new("1")
    assert isinstance(outline.vertex_count, Constant2)
    assert outline.vertex_count.value == Offset.new("3")

    assert isinstance(outline.start_x, Constant2)
    assert outline.start_x.value == Offset.new("1")

    assert isinstance(outline.start_y, Negation2)
    assert isinstance(outline.start_y.op, Constant2)
    assert outline.start_y.op.value == Offset.new("1")

    assert isinstance(outline.points[0].x, Constant2)
    assert outline.points[0].x.value == Offset.new("1")

    assert isinstance(outline.points[0].y, Constant2)
    assert outline.points[0].y.value == Offset.new("1")

    assert isinstance(outline.points[1].x, Constant2)
    assert outline.points[1].x.value == Offset.new("2")

    assert isinstance(outline.points[1].y, Constant2)
    assert outline.points[1].y.value == Offset.new("1")

    assert isinstance(outline.points[2].x, Constant2)
    assert outline.points[2].x.value == Offset.new("1")

    assert isinstance(outline.points[2].y, Negation2)
    assert isinstance(outline.points[2].y.op, Constant2)
    assert outline.points[2].y.op.value == Offset.new("1")

    assert isinstance(outline.rotation, Constant2)
    assert outline.rotation.value == Offset.new("30")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_one_code_5_polygon() -> None:
    gerber_source = """
    %AMPolygon*
    5,1,8,0,0,8,0*%
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Polygon")
    assert macro.name == "Polygon"
    assert len(macro.statements) == 1

    poly = macro.statements[0]
    assert isinstance(poly, Code5Polygon2)

    assert isinstance(poly.exposure, Constant2)
    assert poly.exposure.value == Offset.new("1")

    assert isinstance(poly.number_of_vertices, Constant2)
    assert poly.number_of_vertices.value == Offset.new("8")

    assert isinstance(poly.center_x, Constant2)
    assert poly.center_x.value == Offset.new("0")

    assert isinstance(poly.center_y, Constant2)
    assert poly.center_y.value == Offset.new("0")

    assert isinstance(poly.diameter, Constant2)
    assert poly.diameter.value == Offset.new("8")

    assert isinstance(poly.rotation, Constant2)
    assert poly.rotation.value == Offset.new("0")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_one_code_7_thermal() -> None:
    gerber_source = """
    %AMThermal*
    7,0,0,0.95,0.75,0.175,0.0*%
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Thermal")
    assert macro.name == "Thermal"
    assert len(macro.statements) == 1

    thermal = macro.statements[0]
    assert isinstance(thermal, Code7Thermal2)

    assert isinstance(thermal.center_x, Constant2)
    assert thermal.center_x.value == Offset.new("0")

    assert isinstance(thermal.center_y, Constant2)
    assert thermal.center_y.value == Offset.new("0")

    assert isinstance(thermal.outer_diameter, Constant2)
    assert thermal.outer_diameter.value == Offset.new("0.95")

    assert isinstance(thermal.inner_diameter, Constant2)
    assert thermal.inner_diameter.value == Offset.new("0.75")

    assert isinstance(thermal.gap, Constant2)
    assert thermal.gap.value == Offset.new("0.175")

    assert isinstance(thermal.rotation, Constant2)
    assert thermal.rotation.value == Offset.new("0.0")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_one_code_20_vector_line() -> None:
    gerber_source = """
    %AMLine*
    20,1,0.9,0,0.45,12,0.45,0*
    %
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Line")

    assert macro.name == "Line"
    assert len(macro.statements) == 1

    vl = macro.statements[0]

    assert isinstance(vl, Code20VectorLine2)
    assert isinstance(vl.exposure, Constant2)
    assert vl.exposure.value == Offset.new("1")
    assert isinstance(vl.width, Constant2)
    assert vl.width.value == Offset.new("0.9")
    assert isinstance(vl.start_x, Constant2)
    assert vl.start_x.value == Offset.new("0")
    assert isinstance(vl.start_y, Constant2)
    assert vl.start_y.value == Offset.new("0.45")
    assert isinstance(vl.end_x, Constant2)
    assert vl.end_x.value == Offset.new("12")
    assert isinstance(vl.end_y, Constant2)
    assert vl.end_y.value == Offset.new("0.45")
    assert isinstance(vl.rotation, Constant2)
    assert vl.rotation.value == Offset.new("0")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_one_code_21_center_line() -> None:
    gerber_source = """
    %AMRECTANGLE*
    21,1,6.8,1.2,3.4,0.6,30*%
    """
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("RECTANGLE")
    assert macro.name == "RECTANGLE"
    assert len(macro.statements) == 1

    center_line = macro.statements[0]
    assert isinstance(center_line, Code21CenterLine2)

    assert isinstance(center_line.exposure, Constant2)
    assert center_line.exposure.value == Offset.new("1")
    assert isinstance(center_line.width, Constant2)
    assert center_line.width.value == Offset.new("6.8")
    assert isinstance(center_line.height, Constant2)
    assert center_line.height.value == Offset.new("1.2")
    assert isinstance(center_line.center_x, Constant2)
    assert center_line.center_x.value == Offset.new("3.4")
    assert isinstance(center_line.center_y, Constant2)
    assert center_line.center_y.value == Offset.new("0.6")
    assert isinstance(center_line.rotation, Constant2)
    assert center_line.rotation.value == Offset.new("30")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_with_variables() -> None:
    gerber_source = """
    %AMRect*
    21,1,$1,$2-2x$3,-$4,-$5+$2,0*%
    """
    expected_statement_count = 1
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Rect")
    assert macro.name == "Rect"
    assert len(macro.statements) == expected_statement_count

    stmt = macro.statements[0]
    assert isinstance(stmt, Code21CenterLine2)

    assert isinstance(stmt.exposure, Constant2)
    assert stmt.exposure.value == Offset.new("1.0")

    assert isinstance(stmt.width, VariableName2)
    assert stmt.width.name == "$1"

    assert isinstance(stmt.height, Subtraction2)
    assert isinstance(stmt.height.lhs, VariableName2)
    assert stmt.height.lhs.name == "$2"

    assert isinstance(stmt.height.rhs, Multiplication2)
    assert isinstance(stmt.height.rhs.lhs, Constant2)
    assert stmt.height.rhs.lhs.value == Offset.new("2")

    assert isinstance(stmt.height.rhs.rhs, VariableName2)
    assert stmt.height.rhs.rhs.name == "$3"

    assert isinstance(stmt.center_x, Negation2)
    assert isinstance(stmt.center_x.op, VariableName2)
    assert stmt.center_x.op.name == "$4"

    assert isinstance(stmt.center_y, Addition2)
    assert isinstance(stmt.center_y.lhs, Negation2)
    assert isinstance(stmt.center_y.lhs.op, VariableName2)
    assert stmt.center_y.lhs.op.name == "$5"
    assert isinstance(stmt.center_y.rhs, VariableName2)
    assert stmt.center_y.rhs.name == "$2"

    assert isinstance(stmt.rotation, Constant2)
    assert stmt.rotation.value == Offset.new("0")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_assignment() -> None:
    gerber_source = """
    %AMDONUTCAL*
    1,1,$1,$2,$3*
    $4=$1x1.25*
    1,0,$4,$2,$3*%
    """
    expected_statement_count = 3
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("DONUTCAL")
    assert macro.name == "DONUTCAL"
    assert len(macro.statements) == expected_statement_count

    stmt = macro.statements[0]
    assert isinstance(stmt, Code1Circle2)

    stmt = macro.statements[1]
    assert isinstance(stmt, Assignment2)

    assert stmt.variable_name == "$4"
    assert isinstance(stmt.value, Multiplication2)
    assert isinstance(stmt.value.lhs, VariableName2)
    assert isinstance(stmt.value.rhs, Constant2)
    assert stmt.value.rhs.value == Offset.new("1.25")

    stmt = macro.statements[2]
    assert isinstance(stmt, Code1Circle2)

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_one_circle.__qualname__,
    )


def test_macro_definition_token_hooks_box_macro() -> None:
    gerber_source = """
    %AMBox*
    0 Rectangle with rounded corners, with rotation*
    0 The origin of the aperture is its center*
    0 $1 X-size*
    0 $2 Y-size*
    0 $3 Rounding radius*
    0 $4 Rotation angle, in degrees counterclockwise*
    0 Add two overlapping rectangle primitives as box body*
    21,1,$1,$2-$3-$3,0,0,$4*
    21,1,$1-$3-$3,$2,0,0,$4*
    0 Add four circle primitives for the rounded corners*
    $5=$1/2*
    $6=$2/2*
    $7=2x$3*
    1,1,$7,$5-$3,$6-$3,$4*
    1,1,$7,-$5+$3,$6-$3,$4*
    1,1,$7,-$5+$3,-$6+$3,$4*
    1,1,$7,$5-$3,-$6+$3,$4*
    %
    """
    expected_statement_count = 9
    context = Parser2Context()
    context.set_draw_units(Unit.Millimeters)

    parse_code(gerber_source, context)

    macro = context.get_macro("Box")
    assert macro.name == "Box"
    assert len(macro.statements) == expected_statement_count

    stmt = macro.statements[0]
    assert isinstance(stmt, Code21CenterLine2)

    stmt = macro.statements[1]
    assert isinstance(stmt, Code21CenterLine2)

    stmt = macro.statements[2]
    assert isinstance(stmt, Assignment2)

    stmt = macro.statements[3]
    assert isinstance(stmt, Assignment2)

    stmt = macro.statements[4]
    assert isinstance(stmt, Assignment2)

    stmt = macro.statements[5]
    assert isinstance(stmt, Code1Circle2)

    stmt = macro.statements[6]
    assert isinstance(stmt, Code1Circle2)

    stmt = macro.statements[7]
    assert isinstance(stmt, Code1Circle2)

    stmt = macro.statements[8]
    assert isinstance(stmt, Code1Circle2)

    assert isinstance(stmt.diameter, VariableName2)
    assert stmt.diameter.name == "$7"

    assert isinstance(stmt.center_x, Subtraction2)
    assert isinstance(stmt.center_x.lhs, VariableName2)
    assert stmt.center_x.lhs.name == "$5"
    assert isinstance(stmt.center_x.rhs, VariableName2)
    assert stmt.center_x.rhs.name == "$3"

    assert isinstance(stmt.center_y, Addition2)
    assert isinstance(stmt.center_y.lhs, Negation2)
    assert isinstance(stmt.center_y.lhs.op, VariableName2)
    assert stmt.center_y.lhs.op.name == "$6"
    assert isinstance(stmt.center_y.rhs, VariableName2)
    assert stmt.center_y.rhs.name == "$3"

    assert isinstance(stmt.rotation, VariableName2)
    assert stmt.rotation.name == "$4"

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_macro_definition_token_hooks_box_macro.__qualname__,
    )


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
    context.push_block_state()
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

    aperture = context.get_aperture(ApertureID("D20"), ApertureTransform())
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

    aperture = context.get_aperture(ApertureID("D17"), ApertureTransform())
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

    aperture = context.get_aperture(ApertureID("D17"), ApertureTransform())
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

    aperture = context.get_aperture(ApertureID("D17"), ApertureTransform())
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

    aperture = context.get_aperture(ApertureID("D17"), ApertureTransform())
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
    current_aperture_id = ApertureID("D11")
    end_point = Vector2D(x=Offset.new("151.892000"), y=Offset.new("-57.6580000"))
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_aperture(current_aperture_id, current_aperture)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Line2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("0.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Line2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
    start_point = Vector2D(x=Offset.new("156.019500"), y=Offset.new("156.019500"))
    center_point = Vector2D(x=Offset.new("156.486139"), y=Offset.new("154.744598"))
    end_point = Vector2D(x=Offset.new("156.019500"), y=Offset.new("-66.357500"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
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
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
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
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Arc2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("0.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("6.0"))

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_aperture(current_aperture_id, current_aperture)
    context.set_current_position(start_point)

    parse_code(gerber_source, context)
    cmds = context.main_command_buffer.get_readonly()

    assert len(cmds) == 1
    cmd = next(iter(cmds))
    assert isinstance(cmd, Flash2)
    assert cmd.attributes == ObjectAttributes()
    assert cmd.transform.polarity == polarity
    assert cmd.aperture == current_aperture
    assert cmd.flash_point == end_point
    assert context.get_current_position() == end_point

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR / test_command_draw_line_token_hooks.__qualname__,
    )


@pytest.mark.xfail(
    reason="For now selecting non-existing aperture does not raise an error, we need a warning system.",
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


@pytest.mark.xfail()
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
            IncrementalCoordinatesNotSupported2Error,
        )
    else:
        pytest.fail("Not raised OnUpdateDrawingState2Error")

    debug_dump_context(
        context,
        DEBUG_DUMP_DIR
        / test_coordinate_format_token_hooks_incremental_leading.__qualname__,
    )


@pytest.mark.xfail()
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
            ZeroOmissionNotSupported2Error,
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
    current_aperture_id = ApertureID("D11")
    current_aperture = Circle2(
        identifier=current_aperture_id,
        diameter=Offset.new("10"),
        hole_diameter=None,
    )
    start_point = Vector2D(x=Offset.new("0.0"), y=Offset.new("6.0"))
    end_point = Vector2D(x=Offset.new("6.0"), y=Offset.new("0.0"))
    expected_command_count = 6

    context = Parser2Context()
    context.set_draw_units(unit)
    context.set_is_multi_quadrant(is_multi_quadrant)
    context.set_draw_mode(draw_mode)
    context.set_coordinate_parser(coordinate_parser)
    context.set_polarity(polarity)
    context.set_current_aperture_id(current_aperture_id)
    context.set_current_position(start_point)
    context.set_aperture(current_aperture_id, current_aperture)

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
                assert cmd.transform.polarity == polarity
                assert cmd.aperture == current_aperture
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
