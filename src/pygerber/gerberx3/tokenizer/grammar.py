"""GerberX3 grammar."""
from __future__ import annotations

from pyparsing import (
    CharsNotIn,
    Combine,
    Forward,
    Literal,
    OneOrMore,
    OpAssoc,
    Opt,
    ParserElement,
    Regex,
    Suppress,
    Word,
    ZeroOrMore,
    infix_notation,
    nums,
    oneOf,
)

from pygerber.gerberx3.tokenizer.tokens.ab_block_aperture import (
    BlockApertureBegin,
    BlockApertureEnd,
)
from pygerber.gerberx3.tokenizer.tokens.ad_define_aperture import DefineAperture
from pygerber.gerberx3.tokenizer.tokens.d01_draw import D01Draw
from pygerber.gerberx3.tokenizer.tokens.d02_move import D02Move
from pygerber.gerberx3.tokenizer.tokens.d03_flash import D03Flash
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import CoordinateFormat
from pygerber.gerberx3.tokenizer.tokens.g01_set_linear import SetLinear
from pygerber.gerberx3.tokenizer.tokens.g02_set_clockwise_circular import (
    SetClockwiseCircular,
)
from pygerber.gerberx3.tokenizer.tokens.g03_set_counterclockwise_circular import (
    SetCounterclockwiseCircular,
)
from pygerber.gerberx3.tokenizer.tokens.g04_comment import Comment
from pygerber.gerberx3.tokenizer.tokens.g3n_region import BeginRegion, EndRegion
from pygerber.gerberx3.tokenizer.tokens.g70_set_unit_inch import SetUnitInch
from pygerber.gerberx3.tokenizer.tokens.g71_set_unit_mm import SetUnitMillimeters
from pygerber.gerberx3.tokenizer.tokens.g75_multi_quadrant import SetMultiQuadrantMode
from pygerber.gerberx3.tokenizer.tokens.g90_set_coordinate_absolute import (
    SetAbsoluteNotation,
)
from pygerber.gerberx3.tokenizer.tokens.g91_set_coordinate_incremental import (
    SetIncrementalNotation,
)
from pygerber.gerberx3.tokenizer.tokens.ip_image_polarity import ImagePolarity
from pygerber.gerberx3.tokenizer.tokens.lm_load_mirroring import LoadMirroring
from pygerber.gerberx3.tokenizer.tokens.ln_load_name import LoadName
from pygerber.gerberx3.tokenizer.tokens.lp_load_polarity import LoadPolarity
from pygerber.gerberx3.tokenizer.tokens.lr_load_rotation import LoadRotation
from pygerber.gerberx3.tokenizer.tokens.ls_load_scaling import LoadScaling
from pygerber.gerberx3.tokenizer.tokens.m00_program_stop import M00ProgramStop
from pygerber.gerberx3.tokenizer.tokens.m01_optional_stop import M01OptionalStop
from pygerber.gerberx3.tokenizer.tokens.m02_end_of_file import M02EndOfFile
from pygerber.gerberx3.tokenizer.tokens.macro.am_macro import MacroDefinition
from pygerber.gerberx3.tokenizer.tokens.macro.arithmetic_expression import (
    ArithmeticExpression,
    NumericConstant,
)
from pygerber.gerberx3.tokenizer.tokens.macro.comment import MacroComment
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point
from pygerber.gerberx3.tokenizer.tokens.macro.primitives import (
    PrimitiveCenterLine,
    PrimitiveCircle,
    PrimitiveOutline,
    PrimitivePolygon,
    PrimitiveThermal,
    PrimitiveVectorLine,
)
from pygerber.gerberx3.tokenizer.tokens.macro.variable_definition import (
    MacroVariableDefinition,
)
from pygerber.gerberx3.tokenizer.tokens.macro.variable_name import MacroVariableName
from pygerber.gerberx3.tokenizer.tokens.mo_unit_mode import UnitMode
from pygerber.gerberx3.tokenizer.tokens.sr_step_repeat import (
    StepRepeatBegin,
    StepRepeatEnd,
)
from pygerber.gerberx3.tokenizer.tokens.tx_attributes import (
    ApertureAttribute,
    DeleteAttribute,
    FileAttribute,
    ObjectAttribute,
)

EOEX = Suppress(Literal("*").set_name("end of expression"))
SOSTMT = Suppress(Literal("%").set_name("start of statement"))
EOSTMT = Suppress(Literal("%").set_name("end of statement"))


def wrap_statement(expr: ParserElement, *, eoex: bool = True) -> ParserElement:
    """Wrap statement in start of statement (%) and end of statement (*%) symbols."""
    return SOSTMT + expr + ((EOEX + EOSTMT) if eoex else EOSTMT)


positive_integer = Word("123456789", nums).set_name("positive integer")
integer = Combine(Opt(oneOf("+ -")) + Word(nums)).set_name("integer")
decimal = Combine(
    Opt(oneOf("+ -")) + (Opt(Word(nums)) + "." + Opt(Word(nums)) | Word(nums)),
).set_name("decimal")

aperture_identifier = (
    Combine("D" + Regex(r"[1-9][0-9]+"))
    .set_name("aperture identifier")
    .set_results_name("aperture_identifier")
)

name = Regex(r"[._a-zA-Z$][._a-zA-Z0-9]*").set_name("name")
user_name = Regex(r"/[_a-zA-Z$][._a-zA-Z0-9]*/").set_name("user name")
string = CharsNotIn("%*").set_name("string")
field = (
    CharsNotIn("%*,").set_name("field").set_results_name("field", list_all_matches=True)
)

file_attribute_name = (
    oneOf(
        ".Part .FileFunction .FilePolarity .SameCoordinates .CreationDate\
        .GenerationSoftware .ProjectId .MD5",
    )
    | user_name
).set_name("file_attribute_name")
aperture_attribute_name = (
    oneOf(".AperFunction .DrillTolerance .FlashText") | user_name
).set_name("aperture_attribute_name")
object_attribute_name = (
    oneOf(
        ".N .P .C .CRot .CMfr .CMPN .CVal .CMnt .CFtp .CPgN .CPgD .CHgt .CLbN\
        .CLbD .CSup",
    )
    | user_name
).set_name("object_attribute_name")

# Set a file attribute.
TF = FileAttribute.wrap(
    wrap_statement(
        Literal("TF")
        + file_attribute_name.set_results_name("file_attribute_name")
        + ZeroOrMore("," + (field | "")),
    ),
)
# Add an aperture attribute to the dictionary or modify it.
TA = ApertureAttribute.wrap(
    wrap_statement(
        Literal("TA")
        + aperture_attribute_name.set_results_name("aperture_attribute_name")
        + ZeroOrMore("," + (field | "")),
    ),
)
# Add an object attribute to the dictionary or modify it.
TO = ObjectAttribute.wrap(
    wrap_statement(
        Literal("TO")
        + object_attribute_name.set_results_name("object_attribute_name")
        + ZeroOrMore("," + (field | "")),
    ),
)
# Delete one or all attributes in the dictionary.
TD = DeleteAttribute.wrap(
    wrap_statement(
        Literal("TD")
        + Opt(
            file_attribute_name
            | aperture_attribute_name
            | object_attribute_name
            | user_name,
        ).set_results_name("attribute_name"),
    ),
)

# A human readable comment, does not affect the image.
G04 = Comment.wrap(
    Suppress(Literal("G04")) + string.set_results_name("string") + EOEX,
)

macro_variable = MacroVariableName.wrap(
    Regex(r"\$[0-9]*[1-9][0-9]*")("macro_variable_name"),
    use_group=False,
)
numeric_constant = NumericConstant.wrap(
    decimal("numeric_constant_value"),
    use_group=False,
)

arithmetic_expression: ParserElement = infix_notation(
    macro_variable | numeric_constant,
    [
        (oneOf("+ -"), 1, OpAssoc.RIGHT, ArithmeticExpression.new),
        (oneOf("x X /"), 2, OpAssoc.LEFT, ArithmeticExpression.new),
        (oneOf("+ -"), 2, OpAssoc.LEFT, ArithmeticExpression.new),
    ],
).set_name("arithmetic expression")


expr = (arithmetic_expression | macro_variable | numeric_constant).set_name(
    "macro body expression.",
)


cs = Suppress(Literal(",").set_name("comma"))

primitive = (
    MacroComment.wrap("0" + string.set_results_name("string"))
    | PrimitiveCircle.wrap(
        "1"  # Circle
        + cs
        + expr.set_results_name("exposure")  # Exposure
        + cs
        + expr.set_results_name("diameter")  # Diameter
        + cs
        + expr.set_results_name("center_x")  # Center X
        + cs
        + expr.set_results_name("center_y")  # Center Y
        + Opt(cs + expr.set_results_name("rotation")),  # Rotation
    )
    | PrimitiveVectorLine.wrap(
        "20"  # Vector Line
        + cs
        + expr.set_results_name("exposure")  # Exposure
        + cs
        + expr.set_results_name("width")  # Width
        + cs
        + expr.set_results_name("start_x")  # Start X
        + cs
        + expr.set_results_name("start_y")  # Start Y
        + cs
        + expr.set_results_name("end_x")  # End X
        + cs
        + expr.set_results_name("end_y")  # End Y
        + cs
        + expr.set_results_name("rotation"),  # Rotation
    )
    | PrimitiveCenterLine.wrap(
        "21"  # Center Line
        + cs
        + expr.set_results_name("exposure")  # Exposure
        + cs
        + expr.set_results_name("width")  # Width
        + cs
        + expr.set_results_name("hight")  # Hight
        + cs
        + expr.set_results_name("center_x")  # Center X
        + cs
        + expr.set_results_name("center_y")  # Center Y
        + cs
        + expr.set_results_name("rotation"),  # Rotation
    )
    | PrimitiveOutline.wrap(
        "4"  # Outline
        + cs
        + expr.set_results_name("exposure")  # Exposure
        + cs
        + expr.set_results_name("number_of_vertices")  # Number of vertices
        + cs
        + expr.set_results_name("start_x")  # Start X
        + cs
        + expr.set_results_name("start_y")  # Start Y
        + OneOrMore(  # Subsequent points...
            Point.wrap(
                cs + expr.set_results_name("x") + cs + expr.set_results_name("y"),
                use_group=False,
            ).set_results_name(
                "point",
                list_all_matches=True,
            ),
        )
        + cs
        + expr.set_results_name("rotation"),  # Rotation
    )
    | PrimitivePolygon.wrap(
        "5"  # Polygon
        + cs
        + expr.set_results_name("exposure")  # Exposure
        + cs
        + expr.set_results_name("number_of_vertices")  # Number of vertices
        + cs
        + expr.set_results_name("center_x")  # Center X
        + cs
        + expr.set_results_name("center_y")  # Center Y
        + cs
        + expr.set_results_name("diameter")  # Diameter
        + cs
        + expr.set_results_name("rotation"),  # Rotation
    )
    | PrimitiveThermal.wrap(
        "7"  # Thermal
        + cs
        + expr.set_results_name("center_x")  # Center X
        + cs
        + expr.set_results_name("center_y")  # Center Y
        + cs
        + expr.set_results_name("outer_diameter")  # Outer diameter
        + cs
        + expr.set_results_name("inner_diameter")  # Inner diameter
        + cs
        + expr.set_results_name("gap")  # Gap
        + cs
        + expr.set_results_name("rotation"),  # Rotation
    )
) + EOEX

variable_definition = MacroVariableDefinition.wrap(
    macro_variable + "=" + expr.set_results_name("value") + EOEX,
).set_name("variable definition")

macro_body = (
    (primitive | variable_definition | G04)
    .set_results_name(
        "macro_body",
        list_all_matches=True,
    )
    .set_name("macro body expression")
)[1, ...]

# Defines a macro aperture template.
AM = MacroDefinition.wrap(
    wrap_statement(
        Literal("AM")
        + name.set_results_name("macro_name").set_name("macro name")
        + EOEX
        + macro_body.set_name("macro body"),
        eoex=False,
    ),
)


am_param = decimal.set_results_name("am_param", list_all_matches=True)
# Defines a template-based aperture, assigns a D code to it.
AD = DefineAperture.wrap(
    wrap_statement(
        Literal("AD")
        + aperture_identifier
        + (
            (
                Literal("C").set_results_name("aperture_type")
                + ","
                + decimal.set_results_name("diameter")
                + Opt("X" + decimal.set_results_name("hole_diameter"))
            )
            | (
                Literal("R").set_results_name("aperture_type")
                + ","
                + decimal.set_results_name("x_size")
                + "X"
                + decimal.set_results_name("y_size")
                + Opt("X" + decimal.set_results_name("hole_diameter"))
            )
            | (
                Literal("O").set_results_name("aperture_type")
                + ","
                + decimal.set_results_name("x_size")
                + "X"
                + decimal.set_results_name("y_size")
                + Opt("X" + decimal.set_results_name("hole_diameter"))
            )
            | (
                Literal("P").set_results_name("aperture_type")
                + ","
                + decimal.set_results_name("outer_diameter")
                + "X"
                + decimal.set_results_name("number_of_vertices")
                + Opt(
                    "X"
                    + decimal.set_results_name("rotation")
                    + Opt("X" + decimal.set_results_name("hole_diameter")),
                )
            )
            | (
                name.set_results_name("aperture_type")
                + Opt("," + am_param + ZeroOrMore("X" + am_param))
            )
        ),
    ),
)

LN = LoadName.wrap(
    wrap_statement(Literal("LN") + string.set_results_name("string")),
)
"""
### Load Name (LN)

Note: The LN command was deprecated in revision I4 from October 2013.

The historic `LN` command doesn't influence the image in any manner and can safely be
overlooked.

Function of the `LN` command:
- `LN` is designed to allocate a name to the following section of the file.
- It was originally conceptualized to serve as a human-readable comment.
- For creating human-readable comments, it's advisable to utilize the standard `G04`
    command.
- The `LN` command has the flexibility to be executed multiple times within a file.

SPEC: `2023.03` SECTION: `8.1.6`
"""

# Loads the scale object transformation parameter.
LS = LoadScaling.wrap(
    wrap_statement(Literal("LS") + decimal.set_results_name("scaling")),
)
"""
### LS Command: Scaling Graphics State Parameter

The `LS` command is employed to establish the scaling graphics state parameter.

Functionality:
- The command dictates the scale factor utilized during object creation.
- The aperture undergoes scaling, anchored at its origin. It's crucial to note that this
    origin might not always align with its geometric center.

Usage and Persistence:
- The `LS` command can be invoked multiple times within a single file.
- Once set, the object scaling retains its value unless a subsequent `LS` command
    modifies it.
- The scaling gets adjusted based on the specific value mentioned in the command and
    doesn't accumulate with the preceding scale factor.

The LS command was introduced in revision 2016.12.

SPEC: `2023.03` SECTION: `4.9.5`
"""
LR = LoadRotation.wrap(
    wrap_statement(Literal("LR") + decimal.set_results_name("rotation")),
)
"""
### LR Command: Rotation Graphics State Parameter

The `LR` command is utilized to configure the rotation graphics state parameter.

Functionality:
- This command specifies the rotation angle to be applied when crafting objects.
- The aperture is rotated centered on its origin, which might either coincide with or
    differ from its geometric center.

Usage and Persistence:
- The `LR` command can be invoked numerous times throughout a file.
- Once defined, the object rotation retains its configuration unless overridden by an
    ensuing `LR` command.
- Rotation is strictly determined by the exact value mentioned in the command and
    doesn't integrate with any prior rotation values.

The LR command was introduced in revision 2016.12.

SPEC: `2023.03` SECTION: `4.9.4`
"""
LM = LoadMirroring.wrap(
    wrap_statement(Literal("LM") + oneOf("N XY Y X").set_results_name("mirroring")),
)
# Loads the polarity object transformation parameter.
LP = LoadPolarity.wrap(
    wrap_statement(Literal("LP") + oneOf("C D").set_results_name("polarity")),
)
# Sets the polarity of the whole image.
IP = ImagePolarity.wrap(
    wrap_statement(
        Literal("POS") + oneOf("POS NEG").set_results_name("image_polarity"),
    ),
)

# End of file.
M02 = M02EndOfFile.wrap(Literal("M02").set_name("End of file") + EOEX)
# Optional stop.
M01 = M01OptionalStop.wrap(Literal("M01").set_name("Optional stop") + EOEX)
# Program stop.
M00 = M00ProgramStop.wrap(Literal("M00").set_name("Program stop") + EOEX)

DNN = DNNSelectAperture.wrap(aperture_identifier + EOEX)
"""Sets the current aperture to D code nn."""

G54DNN = DNNSelectAperture.wrap(Literal("G54") + aperture_identifier + EOEX)
"""Sets the current aperture to D code nn."""


G01 = SetLinear.wrap(oneOf("G1 G01 G001 G0001") + EOEX)
"""# Sets linear/circular mode to linear."""

G02 = SetClockwiseCircular.wrap(oneOf("G2 G02 G002 G0002") + EOEX)
"""Sets linear/circular mode to clockwise circular."""

G03 = SetCounterclockwiseCircular.wrap(oneOf("G3 G03 G003 G0003") + EOEX)
"""Sets linear/circular mode to counterclockwise circular."""

G70 = SetUnitInch.wrap(Literal("G70") + EOEX)
"""DEPRECATED: Set the `Unit` to inch."""

G71 = SetUnitMillimeters.wrap(Literal("G71") + EOEX)
"""DEPRECATED: Set the `Unit` to millimeter."""

G74 = SetMultiQuadrantMode.wrap(Literal("G74") + EOEX)
"""DEPRECATED: Set's single quadrant mode."""

G75 = SetMultiQuadrantMode.wrap(Literal("G75") + EOEX)
"""Set's multi quadrant mode."""

G90 = SetAbsoluteNotation.wrap(Literal("G90") + EOEX)
"""Set the `Coordinate format` to `Absolute notation`."""

G91 = SetIncrementalNotation.wrap(Literal("G91") + EOEX)
"""Set the `Coordinate format` to `Incremental notation`."""

X_coordinate = Literal("X") + integer.set_results_name("x").set_name("X coordinate")
Y_coordinate = Literal("Y") + integer.set_results_name("y").set_name("Y coordinate")

I_coordinate = Literal("I") + integer.set_results_name("i").set_name("I offset")
J_coordinate = Literal("J") + integer.set_results_name("j").set_name("J offset")

XY = (X_coordinate + Opt(Y_coordinate)) | (Opt(X_coordinate) + Y_coordinate)
IJ = (I_coordinate + Opt(J_coordinate)) | (Opt(I_coordinate) + J_coordinate)

# Creates a flash object with the current aperture. The
# current point is moved to the flash point.
D03 = D03Flash.wrap(
    Opt(XY) + oneOf("D3 D03 D003 D0003") + EOEX,
)
# D02 moves the current point to the coordinate in the
# command. It does not create an object.
D02 = D02Move.wrap(
    Opt(XY) + oneOf("D2 D02 D002 D0002") + EOEX,
)
# Outside a region statement D01 creates a draw or arc
# object with the current aperture. Inside it adds a draw/arc
# segment to the contour under construction. The current
# point is moved to draw/arc end point after the creation of
# the draw/arc.
D01 = D01Draw.wrap(
    ((Opt(XY) + Opt(IJ) + oneOf("D1 D01 D001 D0001")) | (XY + Opt(IJ))) + EOEX,
)

coord_digits = Regex(r"[1-6][1-6]")

# Sets the coordinate format, e.g. the number of decimals.
FS = CoordinateFormat.wrap(
    wrap_statement(
        Literal("FS")
        + oneOf("L T").set_results_name("zeros_mode").set_name("zeros mode")
        + oneOf("A I").set_results_name("coordinate_mode").set_name("coordinate mode")
        + "X"
        + coord_digits.set_results_name("x_format").set_name("X coordinate format")
        + "Y"
        + coord_digits.set_results_name("y_format").set_name("Y coordinate format"),
    ),
)
# Sets the unit to mm or inch.
MO = UnitMode.wrap(
    wrap_statement(
        Literal("MO") + oneOf("MM IN").set_results_name("unit").set_name("unit"),
    ),
)

# Starts a region statement which creates a region by defining its contours.
G36 = BeginRegion.wrap(Literal("G36") + EOEX)
# Ends the region statement.
G37 = EndRegion.wrap(Literal("G37") + EOEX)

AB_statement = Forward()
SR_statement = Forward()

block = Forward()
block <<= ZeroOrMore(
    G04
    | AD
    | AM
    | DNN
    | G54DNN
    | D01
    | D02
    | D03
    | G01
    | G02
    | G03
    | G75
    | G74
    | LP
    | LM
    | LR
    | LS
    | G36
    | G37
    | AB_statement
    | TF
    | TA
    | TO
    | TD,
)

# Open a step and repeat statement.
SR_open = StepRepeatBegin.wrap(
    wrap_statement(
        Literal("SR")
        + "X"
        + positive_integer.set_results_name("x_repeat")
        + "Y"
        + positive_integer.set_results_name("y_repeat")
        + "I"
        + decimal.set_results_name("x_step")
        + "J"
        + decimal.set_results_name("y_step"),
    ),
)
# Closes a step and repeat statement.
SR_close = StepRepeatEnd.wrap(wrap_statement(Literal("SR")))
SR_statement <<= SR_open + block + SR_close

# Opens a block aperture statement and assigns its aperture number
AB_open = BlockApertureBegin.wrap(wrap_statement(Literal("AB") + aperture_identifier))
# Closes a block aperture statement.
AB_close = BlockApertureEnd.wrap(wrap_statement(Literal("AB")))
AB_statement <<= AB_open + block + AB_close

common = (
    G04
    | MO
    | FS
    | AD
    | AM
    | DNN
    | G54DNN
    | D01
    | D02
    | D03
    | G01
    | G02
    | G03
    | G70
    | G71
    | G74
    | G75
    | G90
    | G91
    | LP
    | LM
    | LR
    | LS
    | LN
    | G36
    | G37
    | AB_statement
    | SR_statement
    | TF
    | TA
    | TO
    | TD
)

_G01 = SetLinear.wrap(Literal("G01"))
_G02 = SetClockwiseCircular.wrap(Literal("G02"))
_G03 = SetCounterclockwiseCircular.wrap(Literal("G03"))
_G70 = SetUnitInch.wrap(Literal("G70"))
_G71 = SetUnitMillimeters.wrap(Literal("G71"))

for g_op in [_G01, _G02, _G03, _G70, _G71]:
    for d_op in [D01, D02, D03]:
        common |= g_op + d_op

EXPRESSIONS = (common | M02 | M01 | M00)[0, ...]
GRAMMAR = common[0, ...] + (M02 | M01 | M00)
