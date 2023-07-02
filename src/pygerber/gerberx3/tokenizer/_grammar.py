"""GerberX3 grammar."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.comment import Comment
from pygerber.gerberx3.tokenizer.tokens.coordinate_format import CoordinateFormat
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

EOEX = Suppress(Literal("*"))  # End of expression.
SOSTMT = Suppress(Literal("%"))  # Start of statement.
EOSTMT = Suppress(Literal("*%"))  # End of statement.


def wrap_statement(expr: ParserElement) -> ParserElement:
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

aperture_identifier = Combine(
    "D" + Word(nums).set_parse_action(lambda t: int(t[0])),
).set_name("aperture identifier")

name = Regex(r"[._a-zA-Z$][._a-zA-Z0-9]*").set_name("name")
user_name = Regex(r"/[_a-zA-Z$][._a-zA-Z0-9]*/").set_name("user name")
string = CharsNotIn("%*").set_name("string")
field = CharsNotIn("%*,").set_name("field")

file_attribute_name = (
    oneOf(
        ".Part .FileFunction .FilePolarity .SameCoordinates .CreationDate\
        .GenerationSoftware .ProjectId .MD5",
    )
    | user_name
)
aperture_attribute_name = oneOf(".AperFunction .DrillTolerance .FlashText") | user_name
object_attribute_name = (
    oneOf(
        ".N .P .C .CRot .CMfr .CMPN .CVal .CMnt .CFtp .CPgN .CPgD .CHgt .CLbN\
        .CLbD .CSup",
    )
    | user_name
)
# Set a file attribute.
TF = Group(
    SOSTMT + Literal("TF") + file_attribute_name + ZeroOrMore("," + field) + EOSTMT,
)
# Add an aperture attribute to the dictionary or modify it.
TA = SOSTMT + Literal("TA") + aperture_attribute_name + ZeroOrMore("," + field) + EOSTMT
# Add an object attribute to the dictionary or modify it.
TO = SOSTMT + Literal("TO") + object_attribute_name + ZeroOrMore("," + field) + EOSTMT
# Delete one or all attributes in the dictionary.
TD = (
    SOSTMT
    + Literal("TD")
    + (
        file_attribute_name
        | aperture_attribute_name
        | object_attribute_name
        | user_name
    )
    + EOSTMT
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

# Defines a template-based aperture, assigns a D code to it.
AD = wrap_statement(
    Literal("AD")
    + aperture_identifier
    + Group(
        (Literal("C") + "," + decimal + Opt("X" + decimal))
        | (Literal("R") + "," + decimal + "X" + decimal + Opt("X" + decimal))
        | (Literal("O") + "," + decimal + "X" + decimal + Opt("X" + decimal))
        | (
            Literal("P")
            + ","
            + decimal
            + "X"
            + decimal
            + Opt("X" + decimal + Opt("X" + decimal))
        )
        | (name + Opt("," + decimal + ZeroOrMore("X" + decimal))),
    ),
)

# Loads the scale object transformation parameter.
LS = wrap_statement(Literal("LS") + decimal)
# Loads the rotation object transformation parameter.
LR = wrap_statement(Literal("LR") + decimal)
# Loads the mirror object transformation parameter.
LM = wrap_statement(Literal("LM") + oneOf("N XY Y X"))
# Loads the polarity object transformation parameter.
LP = wrap_statement(Literal("LP") + oneOf("C D"))

# End of file.
M02 = Literal("M02") + EOEX
Dnn = aperture_identifier + EOEX

# A G75 must be called before creating the first arc.
G75 = Literal("G75") + EOEX
# Sets linear/circular mode to counterclockwise circular.
G03 = Literal("G03") + EOEX
# Sets linear/circular mode to clockwise circular.
G02 = Literal("G02") + EOEX
# Sets linear/circular mode to linear.
G01 = Literal("G01") + EOEX

# Creates a flash object with the current aperture. The
# current point is moved to the flash point.
D03 = Opt(Literal("X") + integer) + Opt(Literal("Y") + integer) + "D03" + EOEX
# D02 moves the current point to the coordinate in the
# command. It does not create an object.
D02 = Opt(Literal("X") + integer) + Opt(Literal("Y") + integer) + "D02" + EOEX
# Outside a region statement D01 creates a draw or arc
# object with the current aperture. Inside it adds a draw/arc
# segment to the contour under construction. The current
# point is moved to draw/arc end point after the creation of
# the draw/arc.
D01 = (
    Opt(Literal("X") + integer)
    + Opt(Literal("Y") + integer)
    + Opt(Literal("I") + integer + Literal("J") + integer)
    + "D01"
    + EOEX
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
MO = wrap_statement(Literal("MO") + oneOf("MM IN"))

region_statement = Forward()
AB_statement = Forward()
SR_statement = Forward()

block = Forward()
block <<= ZeroOrMore(
    G04
    | AD
    | AM
    | Dnn
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

SR_open = wrap_statement(
    Literal("SR")
    + "X"
    + positive_integer
    + "Y"
    + positive_integer
    + "I"
    + decimal
    + "J"
    + decimal,
)
SR_close = wrap_statement(Literal("SR"))
SR_statement <<= SR_open + block + SR_close

AB_open = wrap_statement(Literal("AB") + aperture_identifier)
AB_close = wrap_statement(Literal("AB"))
AB_statement <<= AB_open + block + AB_close

G37 = Literal("G37") + EOEX
G36 = Literal("G36") + EOEX
contour = D02 + ZeroOrMore(D01 | G01 | G02 | G03 | G04)
region_statement <<= G36 + OneOrMore(contour | G04) + G37

GRAMMAR = (
    ZeroOrMore(
        G04
        | MO
        | FS
        | AD
        | AM
        | Dnn
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
