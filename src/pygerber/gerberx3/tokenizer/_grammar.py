"""GerberX3 grammar."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.comment import Comment
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

TF = Group(
    SOSTMT + Literal("TF") + file_attribute_name + ZeroOrMore("," + field) + EOSTMT,
).add_parse_action()
TA = SOSTMT + Literal("TA") + aperture_attribute_name + ZeroOrMore("," + field) + EOSTMT
TO = SOSTMT + Literal("TO") + object_attribute_name + ZeroOrMore("," + field) + EOSTMT
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

G04 = Comment.wrap(Suppress(Literal("G04")) + string("string") + EOEX)

primitive = Group(oneOf("0 1 20 21 4 5 7") + ZeroOrMore("," + expr) + EOEX)
variable_definition = macro_variable + "=" + expr + EOEX
macro_body = OneOrMore(primitive | variable_definition | G04)
AM = Literal("%AM") + name + EOEX + macro_body + "%"

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

LS = wrap_statement(Literal("LS") + decimal)
LR = wrap_statement(Literal("LR") + decimal)
LM = wrap_statement(Literal("LM") + oneOf("N XY Y X"))
LP = wrap_statement(Literal("LP") + oneOf("C D"))

M02 = Literal("M02") + EOEX
Dnn = aperture_identifier + EOEX

G75 = Literal("G75") + EOEX
G03 = Literal("G03") + EOEX
G02 = Literal("G02") + EOEX
G01 = Literal("G01") + EOEX

D03 = Opt(Literal("X") + integer) + Opt(Literal("Y") + integer) + "D03" + EOEX
D02 = Opt(Literal("X") + integer) + Opt(Literal("Y") + integer) + "D02" + EOEX
D01 = (
    Opt(Literal("X") + integer)
    + Opt(Literal("Y") + integer)
    + Opt(Literal("I") + integer + Literal("J") + integer)
    + "D01"
    + EOEX
)

FS = wrap_statement(
    Literal("FS")
    + "LA"
    + "X"
    + Word("123456", exact=2)
    + "Y"
    + Word("123456", exact=2),
)
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
