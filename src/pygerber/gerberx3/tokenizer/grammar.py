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
from pygerber.gerberx3.tokenizer.tokens.d01_draw import Draw
from pygerber.gerberx3.tokenizer.tokens.d02_move import Move
from pygerber.gerberx3.tokenizer.tokens.d03_flash import Flash
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import CoordinateFormat
from pygerber.gerberx3.tokenizer.tokens.g0n_set_draw_mode import (
    SetClockwiseCircular,
    SetCounterclockwiseCircular,
    SetLinear,
)
from pygerber.gerberx3.tokenizer.tokens.g04_comment import Comment
from pygerber.gerberx3.tokenizer.tokens.g3n_region import BeginRegion, EndRegion
from pygerber.gerberx3.tokenizer.tokens.lm_load_mirroring import LoadMirroring
from pygerber.gerberx3.tokenizer.tokens.lp_load_polarity import LoadPolarity
from pygerber.gerberx3.tokenizer.tokens.lr_load_rotation import LoadRotation
from pygerber.gerberx3.tokenizer.tokens.ls_load_scaling import LoadScaling
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

EOEX = Suppress(Literal("*"))  # End of expression.
SOSTMT = Suppress(Literal("%"))  # Start of statement.
EOSTMT = Suppress(Literal("%"))  # End of statement.


def wrap_statement(expr: ParserElement, *, eoex: bool = True) -> ParserElement:
    """Wrap statement in start of statement (%) and end of statement (*%) symbols."""
    return SOSTMT + expr + ((EOEX + EOSTMT) if eoex else EOSTMT)


unsigned_integer = Word(nums)
positive_integer = Word("123456789", nums)
integer = Combine(Opt(oneOf("+ -")) + Word(nums))
unsigned_decimal = Combine(Opt(Word(nums)) + "." + Opt(Word(nums))) | Word(
    nums,
)
decimal = Combine(
    Opt(oneOf("+ -")) + (Opt(Word(nums)) + "." + Opt(Word(nums)) | Word(nums)),
)

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
    unsigned_decimal("numeric_constant_value"),
    use_group=False,
)

arithmetic_expression: ParserElement = infix_notation(
    macro_variable | numeric_constant,
    [
        (oneOf("x X /"), 2, OpAssoc.LEFT, ArithmeticExpression.new),
        (oneOf("+ -"), 2, OpAssoc.LEFT, ArithmeticExpression.new),
    ],
)


expr = arithmetic_expression | macro_variable | numeric_constant


cs = Suppress(Literal(","))
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
)
macro_body = (
    (primitive | variable_definition | G04).set_results_name(
        "macro_body",
        list_all_matches=True,
    )
)[1, ...]

# Defines a macro aperture template.
AM = MacroDefinition.wrap(
    wrap_statement(
        Literal("AM") + name.set_results_name("macro_name") + EOEX + macro_body,
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

# Loads the scale object transformation parameter.
LS = LoadScaling.wrap(
    wrap_statement(Literal("LS") + decimal.set_results_name("scaling")),
)
# Loads the rotation object transformation parameter.
LR = LoadRotation.wrap(
    wrap_statement(Literal("LR") + decimal.set_results_name("rotation")),
)
# Loads the mirror object transformation parameter.
LM = LoadMirroring.wrap(
    wrap_statement(Literal("LM") + oneOf("N XY Y X").set_results_name("mirroring")),
)
# Loads the polarity object transformation parameter.
LP = LoadPolarity.wrap(
    wrap_statement(Literal("LP") + oneOf("C D").set_results_name("polarity")),
)

# End of file.
M02 = M02EndOfFile.wrap(Literal("M02").set_name("end of file") + EOEX)
# Sets the current aperture to D code nn.
DNN = DNNSelectAperture.wrap(
    aperture_identifier + EOEX,
)

# A G75 must be called before creating the first arc for backwards compatibility,
# but we will ignore that, as it has no real impact on drawing.
G75 = Suppress(Literal("G75") + EOEX)
# Sets linear/circular mode to counterclockwise circular.
G03 = SetCounterclockwiseCircular.wrap(Literal("G03") + EOEX)
# Sets linear/circular mode to clockwise circular.
G02 = SetClockwiseCircular.wrap(Literal("G02") + EOEX)
# Sets linear/circular mode to linear.
G01 = SetLinear.wrap(Literal("G01") + EOEX)

# Creates a flash object with the current aperture. The
# current point is moved to the flash point.
D03 = Flash.wrap(
    Opt(Literal("X") + integer.set_results_name("x"))
    + Opt(Literal("Y") + integer.set_results_name("y"))
    + "D03"
    + EOEX,
)
# D02 moves the current point to the coordinate in the
# command. It does not create an object.
D02 = Move.wrap(
    Opt(Literal("X") + integer.set_results_name("x"))
    + Opt(Literal("Y") + integer.set_results_name("y"))
    + "D02"
    + EOEX,
)
# Outside a region statement D01 creates a draw or arc
# object with the current aperture. Inside it adds a draw/arc
# segment to the contour under construction. The current
# point is moved to draw/arc end point after the creation of
# the draw/arc.
D01 = Draw.wrap(
    Opt(Literal("X") + integer.set_results_name("x"))
    + Opt(Literal("Y") + integer.set_results_name("y"))
    + Opt(
        Literal("I")
        + integer.set_results_name("i")
        + Literal("J")
        + integer.set_results_name("j"),
    )
    + "D01"
    + EOEX,
)

coord_digits = Regex(r"[1-6][1-6]")

# Sets the coordinate format, e.g. the number of decimals.
FS = CoordinateFormat.wrap(
    wrap_statement(
        Literal("FS")
        + Regex("[LT]").set_results_name("zeros_mode")
        + Regex("[AI]").set_results_name("coordinate_mode")
        + "X"
        + coord_digits.set_results_name("x_format")
        + "Y"
        + coord_digits.set_results_name("y_format"),
    ),
)
# Sets the unit to mm or inch.
MO = UnitMode.wrap(
    wrap_statement(Literal("MO") + oneOf("MM IN").set_results_name("unit")),
)

region_statement = Forward()
AB_statement = Forward()
SR_statement = Forward()

block = Forward()
block <<= ZeroOrMore(
    G04
    | AD
    | AM
    | DNN
    | D01
    | D02
    | D03
    | G01
    | G02
    | G03
    | G75
    | LP
    | LM
    | LR
    | LS
    | region_statement
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

# Starts a region statement which creates a region by defining its contours.
G36 = BeginRegion.wrap(Literal("G36") + EOEX)
# Ends the region statement.
G37 = EndRegion.wrap(Literal("G37") + EOEX)

contour = D02 + ZeroOrMore(D01 | G01 | G02 | G03 | G04)
region_statement <<= G36 + OneOrMore(contour | G04) + G37

EXPRESSIONS = (
    G04
    | MO
    | FS
    | AD
    | AM
    | DNN
    | D01
    | D02
    | D03
    | G01
    | G02
    | G03
    | G75
    | LP
    | LM
    | LR
    | LS
    | region_statement
    | AB_statement
    | SR_statement
    | TF
    | TA
    | TO
    | TD
    | M02
)[0, ...]

GRAMMAR = (
    G04
    | MO
    | FS
    | AD
    | AM
    | DNN
    | D01
    | D02
    | D03
    | G01
    | G02
    | G03
    | G75
    | LP
    | LM
    | LR
    | LS
    | region_statement
    | AB_statement
    | SR_statement
    | TF
    | TA
    | TO
    | TD
)[0, ...] + M02
