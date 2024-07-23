"""`pygerber.gerberx3.parser.pyparsing.grammar` module contains the Gerber X3 grammar
implemented using the pyparsing library.
"""

from __future__ import annotations

from typing import ClassVar, List, Type, TypeVar, cast

import pyparsing as pp
from pydantic import ValidationError

from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
from pygerber.gerberx3.ast.nodes.d_codes.D02 import D02
from pygerber.gerberx3.ast.nodes.d_codes.D03 import D03
from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn
from pygerber.gerberx3.ast.nodes.file import File
from pygerber.gerberx3.ast.nodes.g_codes.G01 import G01
from pygerber.gerberx3.ast.nodes.g_codes.G02 import G02
from pygerber.gerberx3.ast.nodes.g_codes.G03 import G03
from pygerber.gerberx3.ast.nodes.g_codes.G04 import G04
from pygerber.gerberx3.ast.nodes.g_codes.G36 import G36
from pygerber.gerberx3.ast.nodes.g_codes.G37 import G37
from pygerber.gerberx3.ast.nodes.g_codes.G54 import G54
from pygerber.gerberx3.ast.nodes.g_codes.G55 import G55
from pygerber.gerberx3.ast.nodes.g_codes.G70 import G70
from pygerber.gerberx3.ast.nodes.g_codes.G71 import G71
from pygerber.gerberx3.ast.nodes.g_codes.G74 import G74
from pygerber.gerberx3.ast.nodes.g_codes.G75 import G75
from pygerber.gerberx3.ast.nodes.g_codes.G90 import G90
from pygerber.gerberx3.ast.nodes.g_codes.G91 import G91
from pygerber.gerberx3.ast.nodes.m_codes.M00 import M00
from pygerber.gerberx3.ast.nodes.m_codes.M01 import M01
from pygerber.gerberx3.ast.nodes.m_codes.M02 import M02
from pygerber.gerberx3.ast.nodes.math.assignment import Assignment
from pygerber.gerberx3.ast.nodes.math.constant import Constant
from pygerber.gerberx3.ast.nodes.math.expression import Expression
from pygerber.gerberx3.ast.nodes.math.operators.binary.add import Add
from pygerber.gerberx3.ast.nodes.math.operators.binary.div import Div
from pygerber.gerberx3.ast.nodes.math.operators.binary.mul import Mul
from pygerber.gerberx3.ast.nodes.math.operators.binary.sub import Sub
from pygerber.gerberx3.ast.nodes.math.operators.unary.neg import Neg
from pygerber.gerberx3.ast.nodes.math.operators.unary.pos import Pos
from pygerber.gerberx3.ast.nodes.math.point import Point
from pygerber.gerberx3.ast.nodes.math.variable import Variable
from pygerber.gerberx3.ast.nodes.other.command_end import CommandEnd
from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate
from pygerber.gerberx3.ast.nodes.other.extended_command_close import (
    ExtendedCommandClose,
)
from pygerber.gerberx3.ast.nodes.other.extended_command_open import ExtendedCommandOpen
from pygerber.gerberx3.ast.nodes.primitives.code_0 import Code0
from pygerber.gerberx3.ast.nodes.primitives.code_1 import Code1
from pygerber.gerberx3.ast.nodes.primitives.code_2 import Code2
from pygerber.gerberx3.ast.nodes.primitives.code_4 import Code4
from pygerber.gerberx3.ast.nodes.primitives.code_5 import Code5
from pygerber.gerberx3.ast.nodes.primitives.code_6 import Code6
from pygerber.gerberx3.ast.nodes.primitives.code_7 import Code7
from pygerber.gerberx3.ast.nodes.primitives.code_20 import Code20
from pygerber.gerberx3.ast.nodes.primitives.code_21 import Code21
from pygerber.gerberx3.ast.nodes.primitives.code_22 import Code22

T = TypeVar("T", bound=Node)


class Grammar:
    """Internal representation of the Gerber X3 grammar."""

    DEFAULT: ClassVar[pp.ParserElement]

    def __init__(
        self,
        ast_node_class_overrides: dict[str, Type[Node]],
        *,
        enable_packrat: bool = True,
    ) -> None:
        self.ast_node_class_overrides = ast_node_class_overrides
        self.enable_packrat = enable_packrat

    def build(self) -> pp.ParserElement:
        """Build the grammar."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> File:
            return self.get_cls(File)(source=s, location=loc, commands=tokens.as_list())

        root = (
            pp.OneOrMore(
                pp.MatchFirst(
                    [
                        self.g_codes(),
                        self.m_codes(),
                        self.d_codes(),
                        self.macro(),
                        self.command_end,
                    ]
                )
            )
            .set_results_name("root_node")
            .set_parse_action(_)
            .set_debug()
        )
        root.enable_packrat()
        return root

    def d_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing D-codes."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> D01:
            parse_result_token_list = tokens.as_list()
            token_list = cast(list[Coordinate], parse_result_token_list)
            try:
                return self.get_cls(D01)(
                    source=s,
                    location=loc,
                    x=token_list[0],
                    y=token_list[1],
                    i=token_list[2] if len(token_list) >= 4 else None,  # noqa: PLR2004
                    j=token_list[3] if len(token_list) >= 5 else None,  # noqa: PLR2004
                )
            except ValidationError as e:
                raise pp.ParseFatalException(s, loc, "Invalid D01") from e

        d01 = (
            (
                self.coordinate
                + self.coordinate
                + pp.Opt(self.coordinate)
                + pp.Opt(self.coordinate)
                + pp.Regex(r"D0*1")
            )
            .set_parse_action(_)
            .set_name("D01")
        )

        def _(s: str, loc: int, tokens: pp.ParseResults) -> D02:
            parse_result_token_list = tokens.as_list()
            token_list = cast(list[Coordinate], parse_result_token_list)
            try:
                return self.get_cls(D02)(
                    source=s,
                    location=loc,
                    x=token_list[0],
                    y=token_list[1],
                )
            except ValidationError as e:
                raise pp.ParseFatalException(s, loc, "Invalid D02") from e

        d02 = (
            (self.coordinate + self.coordinate + pp.Regex(r"D0*2"))
            .set_parse_action(_)
            .set_name("D02")
        )

        def _(s: str, loc: int, tokens: pp.ParseResults) -> D03:
            parse_result_token_list = tokens.as_list()
            token_list = cast(list[Coordinate], parse_result_token_list)
            try:
                return self.get_cls(D03)(
                    source=s,
                    location=loc,
                    x=token_list[0],
                    y=token_list[1],
                )
            except ValidationError as e:
                raise pp.ParseFatalException(s, loc, "Invalid D03") from e

        d03 = (
            (self.coordinate + self.coordinate + pp.Regex(r"D0*3"))
            .set_parse_action(_)
            .set_name("D03")
        )

        def _(s: str, loc: int, tokens: pp.ParseResults) -> Dnn:
            parse_result_token_list = tokens.as_list()
            token_list = cast(list[Coordinate], parse_result_token_list)
            value = token_list[0]
            assert isinstance(value, str)  # type: ignore[unreachable]
            assert value.startswith("D")  # type: ignore[unreachable]
            assert len(value) > 1

            try:
                return self.get_cls(Dnn)(source=s, location=loc, value=value)
            except ValidationError as e:
                raise pp.ParseFatalException(s, loc, "Invalid Dnn") from e

        dnn = pp.Regex(r"D0*[0-9]*").set_parse_action(_).set_name("Dnn")

        return pp.MatchFirst([d01, d02, d03, dnn])

    def get_cls(self, node_cls: Type[T]) -> Type[T]:
        """Get the class of the node."""
        return self.ast_node_class_overrides.get(node_cls.__qualname__, node_cls)  # type: ignore[return-value]

    @pp.cached_property
    def coordinate(self) -> pp.ParserElement:
        """Create a parser element capable of parsing coordinates."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> Coordinate:
            type_, value = tokens.as_list()
            assert isinstance(type_, str), type(type_)
            assert type_ in ("X", "Y", "I", "J")
            assert isinstance(value, str)

            return self.get_cls(Coordinate)(
                source=s,
                location=loc,
                type=type_,  # type: ignore[arg-type]
                value=value,
            )

        return (
            (
                pp.oneOf(("X", "Y", "I", "J")).set_name("coordinate_type")
                + pp.Regex(r"[+-]?[0-9]+").set_name("coordinate_value")
            )
            .set_parse_action(_)
            .set_name("coordinate")
        )

    @pp.cached_property
    def command_end(self) -> pp.ParserElement:
        """Create a parser element capable of parsing the command end."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> CommandEnd:
            return self.get_cls(CommandEnd)(source=s, location=loc)

        return pp.Literal("*").set_name("*").set_parse_action(_)

    def g_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing G-codes."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> G04:
            content = tokens.as_dict().get("string")
            assert isinstance(content, str)
            return self.get_cls(G04)(source=s, location=loc, content=content)

        g04_comment = (
            (pp.Regex(r"G0*4") + self.string).set_name("G04").set_parse_action(_)
        )

        return pp.MatchFirst(
            [
                g04_comment,
                *(
                    self.g(
                        value,
                        self.get_cls(cls),  # type: ignore[arg-type]
                    )
                    for (value, cls) in reversed(
                        (
                            (1, G01),
                            (2, G02),
                            (3, G03),
                            (4, G04),
                            (36, G36),
                            (37, G37),
                            (54, G54),
                            (55, G55),
                            (70, G70),
                            (71, G71),
                            (74, G74),
                            (75, G75),
                            (90, G90),
                            (91, G91),
                        )
                    )
                ),
            ]
        )

    @pp.cached_property
    def string(self) -> pp.ParserElement:
        """Create a parser element capable of parsing strings."""
        return pp.CharsNotIn("%*").set_results_name("string")

    def g(self, value: int, cls: Type[Node]) -> pp.ParserElement:
        """Create a parser element capable of parsing particular G-code."""
        element = pp.Regex(r"G0*" + str(value)).set_name(f"G{value}")
        return element.setParseAction(
            lambda s, loc, _tokens: self.get_cls(cls)(source=s, location=loc)
        )

    def m_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing M-codes."""
        return pp.MatchFirst(
            [
                self.m(
                    value,
                    self.get_cls(cls),  # type: ignore[arg-type, type-abstract]
                )
                for (value, cls) in (
                    (0, M00),
                    (1, M01),
                    (2, M02),
                )
            ]
        )

    def m(self, value: int, cls: Type[Node]) -> pp.ParserElement:
        """Create a parser element capable of parsing particular D-code."""
        element = pp.Regex(r"M0*" + str(value)).set_name(f"M{value}")
        return element.setParseAction(
            lambda s, loc, _tokens: cls(source=s, location=loc)
        )

    @pp.cached_property
    def extended_command_open(self) -> pp.ParserElement:
        """Create a parser element capable of parsing the extended command open."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> Node:
            return self.get_cls(ExtendedCommandOpen)(source=s, location=loc)

        return pp.Regex(r"%").set_name("%").set_parse_action(_)

    @pp.cached_property
    def extended_command_close(self) -> pp.ParserElement:
        """Create a parser element capable of parsing the extended command close."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> Node:
            return self.get_cls(ExtendedCommandClose)(source=s, location=loc)

        return pp.Regex(r"%").set_name("%").set_parse_action(_)

    def macro(self) -> pp.ParserElement:
        """Create a parser element capable of parsing macros."""

        def _am_open(s: str, loc: int, tokens: pp.ParseResults) -> Node:
            return self.get_cls(AMopen)(source=s, location=loc, **tokens.as_dict())

        def _am_close(s: str, loc: int, tokens: pp.ParseResults) -> Node:
            return self.get_cls(AMclose)(source=s, location=loc, **tokens.as_dict())

        cs = pp.Suppress(pp.Literal(",").set_name("comma"))

        def _point(s: str, loc: int, tokens: pp.ParseResults) -> Point:
            return self.get_cls(Point)(source=s, location=loc, **tokens.as_dict())

        return (
            self.extended_command_open
            + (pp.Literal("AM") + self.name)
            .set_name("AMopen")
            .set_parse_action(_am_open)
            + self.command_end
            + pp.ZeroOrMore(
                pp.MatchFirst(
                    [
                        self.assignment,
                        self.primitive(Code0, 0, self.string),
                        self.primitive(
                            Code1,
                            1,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("diameter")
                            + cs
                            + self.expression.set_results_name("center_x")
                            + cs
                            + self.expression.set_results_name("center_y")
                            + pp.Opt(cs + self.expression.set_results_name("rotation")),
                        ),
                        self.primitive(
                            Code2,
                            2,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("width")
                            + cs
                            + self.expression.set_results_name("start_x")
                            + cs
                            + self.expression.set_results_name("start_y")
                            + cs
                            + self.expression.set_results_name("end_x")
                            + cs
                            + self.expression.set_results_name("end_y")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code4,
                            4,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("number_of_points")
                            + cs
                            + self.expression.set_results_name("start_x")
                            + cs
                            + self.expression.set_results_name("start_y")
                            + pp.OneOrMore(
                                (
                                    cs
                                    + self.expression.set_results_name("x")
                                    + cs
                                    + self.expression.set_results_name("y")
                                )
                                .set_results_name("points", list_all_matches=True)
                                .set_parse_action(_point),
                            )
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code5,
                            5,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("number_of_vertices")
                            + cs
                            + self.expression.set_results_name("center_x")
                            + cs
                            + self.expression.set_results_name("center_y")
                            + cs
                            + self.expression.set_results_name("diameter")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code6,
                            6,
                            cs
                            + self.expression.set_results_name("center_x")
                            + cs
                            + self.expression.set_results_name("center_y")
                            + cs
                            + self.expression.set_results_name("outer_diameter")
                            + cs
                            + self.expression.set_results_name("ring_thickness")
                            + cs
                            + self.expression.set_results_name("gap_between_rings")
                            + cs
                            + self.expression.set_results_name("max_ring_count")
                            + cs
                            + self.expression.set_results_name("crosshair_thickness")
                            + cs
                            + self.expression.set_results_name("crosshair_length")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code7,
                            7,
                            cs
                            + self.expression.set_results_name("center_x")
                            + cs
                            + self.expression.set_results_name("center_y")
                            + cs
                            + self.expression.set_results_name("outer_diameter")
                            + cs
                            + self.expression.set_results_name("inner_diameter")
                            + cs
                            + self.expression.set_results_name("gap_thickness")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code20,
                            20,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("width")
                            + cs
                            + self.expression.set_results_name("start_x")
                            + cs
                            + self.expression.set_results_name("start_y")
                            + cs
                            + self.expression.set_results_name("end_x")
                            + cs
                            + self.expression.set_results_name("end_y")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code21,
                            21,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("width")
                            + cs
                            + self.expression.set_results_name("height")
                            + cs
                            + self.expression.set_results_name("center_x")
                            + cs
                            + self.expression.set_results_name("center_y")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                        self.primitive(
                            Code22,
                            22,
                            cs
                            + self.expression.set_results_name("exposure")
                            + cs
                            + self.expression.set_results_name("width")
                            + cs
                            + self.expression.set_results_name("height")
                            + cs
                            + self.expression.set_results_name("x_lower_left")
                            + cs
                            + self.expression.set_results_name("y_lower_left")
                            + cs
                            + self.expression.set_results_name("rotation"),
                        ),
                    ]
                )
            )
            + (pp.Literal("").set_name("AM_close").set_parse_action(_am_close))
            + self.extended_command_close
        )

    @pp.cached_property
    def name(self) -> pp.ParserElement:
        """Create a parser element capable of parsing names."""
        return pp.Regex(r"[._$a-zA-Z][._$a-zA-Z0-9]{0,126}").set_results_name("name")

    def primitive(
        self, cls: Type[Node], code: int, fields: pp.ParserElement
    ) -> pp.ParserElement:
        """Create a parser element capable of parsing a primitive."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> Node:
            return self.get_cls(cls)(source=s, location=loc, **_tokens.as_dict())

        return (pp.Literal(str(code)) + fields).set_name(
            f"primitive-{code}"
        ).set_parse_action(_) + self.command_end

    @pp.cached_property
    def expression(self) -> pp.ParserElement:
        """Create a parser element capable of parsing expressions."""
        factor = self.constant | self.variable

        def _neg(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            token_list = cast(List[List[Expression]], tokens.as_list())[0]
            assert len(token_list) == 1
            return self.get_cls(Neg)(source=s, location=loc, operand=token_list[0])

        def _pos(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            token_list = cast(List[List[Expression]], tokens.as_list())[0]
            assert len(token_list) == 1
            return self.get_cls(Pos)(source=s, location=loc, operand=token_list[0])

        def _sub(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            nested_token_list = cast(List[List[Expression]], tokens.as_list())
            assert len(nested_token_list) == 1
            token_list = nested_token_list[0]
            assert len(token_list) > 1
            return self.get_cls(Sub)(source=s, location=loc, operands=token_list)

        def _add(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            nested_token_list = cast(List[List[Expression]], tokens.as_list())
            assert len(nested_token_list) == 1
            token_list = nested_token_list[0]
            assert len(token_list) > 1
            return self.get_cls(Add)(source=s, location=loc, operands=token_list)

        def _div(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            nested_token_list = cast(List[List[Expression]], tokens.as_list())
            assert len(nested_token_list) == 1
            token_list = nested_token_list[0]
            assert len(token_list) > 1
            return self.get_cls(Div)(source=s, location=loc, operands=token_list)

        def _mul(s: str, loc: int, tokens: pp.ParseResults) -> Expression:
            nested_token_list = cast(List[List[Expression]], tokens.as_list())
            assert len(nested_token_list) == 1
            token_list = nested_token_list[0]
            assert len(token_list) > 1
            return self.get_cls(Mul)(source=s, location=loc, operands=token_list)

        return pp.infix_notation(
            factor,
            [
                (
                    pp.Suppress("-"),
                    1,
                    pp.OpAssoc.RIGHT,
                    _neg,
                ),
                (
                    pp.Suppress("+"),
                    1,
                    pp.OpAssoc.RIGHT,
                    _pos,
                ),
                (
                    pp.Suppress("/"),
                    2,
                    pp.OpAssoc.LEFT,
                    _div,
                ),
                (
                    pp.Suppress(pp.oneOf("x X")),
                    2,
                    pp.OpAssoc.LEFT,
                    _mul,
                ),
                (
                    pp.Suppress("-"),
                    2,
                    pp.OpAssoc.LEFT,
                    _sub,
                ),
                (
                    pp.Suppress("+"),
                    2,
                    pp.OpAssoc.LEFT,
                    _add,
                ),
            ],
        ).set_name("expression")

    @pp.cached_property
    def constant(self) -> pp.ParserElement:
        """Create a parser element capable of parsing constants."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> Node:
            return self.get_cls(Constant)(source=s, location=loc, **_tokens.as_dict())

        return self.double.set_results_name("constant").set_parse_action(_)

    @pp.cached_property
    def double(self) -> pp.ParserElement:
        """Create a parser element capable of parsing doubles."""
        return pp.Regex(r"[+-]?(([0-9]+(\.[0-9]+)?)|(\.[0-9]+))").set_results_name(
            "double"
        )

    @pp.cached_property
    def variable(self) -> pp.ParserElement:
        """Create a parser element capable of parsing variables."""

        def _(s: str, loc: int, _tokens: pp.ParseResults) -> Node:
            return self.get_cls(Variable)(source=s, location=loc, **_tokens.as_dict())

        return pp.Regex(r"\$[0-9]+").set_results_name("variable").set_parse_action(_)

    @pp.cached_property
    def assignment(self) -> pp.ParserElement:
        """Create a parser element capable of parsing assignments."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> Node:
            return self.get_cls(Assignment)(source=s, location=loc, **tokens.as_dict())

        return (
            self.variable
            + pp.Suppress("=")
            + self.expression.set_results_name("expression")
        ).set_results_name("assignment").set_parse_action(_) + self.command_end


Grammar.DEFAULT = Grammar({}).build()
