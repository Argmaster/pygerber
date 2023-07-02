"""GerberX3 grammar."""
from __future__ import annotations

from pyparsing import (
    CharsNotIn,
    Combine,
    Forward,
    Group,
    Literal,
    OneOrMore,
    Opt,
    ParserElement,
    Regex,
    Suppress,
    Word,
    ZeroOrMore,
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
EOSTMT = Suppress(Literal("*%"))  # End of statement.


def wrap_statement(expr: ParserElement) -> ParserElement:
    """Wrap statement in start of statement (%) and end of statement (*%) symbols."""
    return SOSTMT + expr + EOSTMT


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
    SOSTMT
    + Literal("TF")
    + file_attribute_name.set_results_name("file_attribute_name")
    + ZeroOrMore("," + (field | ""))
    + EOSTMT,
)
# Add an aperture attribute to the dictionary or modify it.
TA = ApertureAttribute.wrap(
    SOSTMT
    + Literal("TA")
    + aperture_attribute_name.set_results_name("aperture_attribute_name")
    + ZeroOrMore("," + (field | ""))
    + EOSTMT,
)
# Add an object attribute to the dictionary or modify it.
TO = ObjectAttribute.wrap(
    SOSTMT
    + Literal("TO")
    + object_attribute_name.set_results_name("object_attribute_name")
    + ZeroOrMore("," + (field | ""))
    + EOSTMT,
)
# Delete one or all attributes in the dictionary.
TD = DeleteAttribute.wrap(
    SOSTMT
    + Literal("TD")
    + Opt(
        file_attribute_name
        | aperture_attribute_name
        | object_attribute_name
        | user_name,
    ).set_results_name("attribute_name")
    + EOSTMT,
)

macro_variable = Regex(r"\$[0-9]*[1-9][0-9]*")
expr = Forward()
factor = Group("(" + expr + ")" | macro_variable | unsigned_decimal)
term = Group(factor + ZeroOrMore(oneOf("x /") + factor))
expr <<= Group(term + ZeroOrMore(oneOf("+ -") + term))

# A human readable comment, does not affect the image.
G04 = Comment.wrap(Suppress(Literal("G04")) + string("string") + EOEX)

primitive = Group(oneOf("0 1 20 21 4 5 7") + ZeroOrMore("," + expr) + EOEX)
variable_definition = macro_variable + "=" + expr + EOEX
macro_body = OneOrMore(primitive | variable_definition | G04)
# Defines a macro aperture template.
AM = Literal("%AM") + name + EOEX + macro_body + "%"


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

GRAMMAR = (
    ZeroOrMore(
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
        | TD,
    )
    + M02
)
