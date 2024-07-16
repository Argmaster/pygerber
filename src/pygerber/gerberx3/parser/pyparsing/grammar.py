"""`pygerber.gerberx3.parser.pyparsing.grammar` module contains the Gerber X3 grammar
implemented using the pyparsing library.
"""

from __future__ import annotations

from typing import ClassVar, Type, TypeVar, cast

import pyparsing as pp
from pydantic import ValidationError

from pygerber.gerberx3.ast.nodes.base import Node
from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
from pygerber.gerberx3.ast.nodes.d_codes.D02 import D02
from pygerber.gerberx3.ast.nodes.d_codes.D03 import D03
from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn
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
from pygerber.gerberx3.ast.nodes.other.coordinate import Coordinate


def g(value: int, cls: Type[Node]) -> pp.ParserElement:
    """Create a parser element capable of parsing particular G-code."""
    element = pp.Regex(r"G0*" + str(value)).set_name(f"G{value}")
    return element.setParseAction(lambda: cls())


def m(value: int, cls: Type[Node]) -> pp.ParserElement:
    """Create a parser element capable of parsing particular D-code."""
    element = pp.Regex(r"M0*" + str(value)).set_name(f"M{value}")
    return element.setParseAction(lambda: cls())


T = TypeVar("T", bound=Node)


class Grammar:
    """Internal representation of the Gerber X3 grammar."""

    DEFAULT: ClassVar[pp.ParserElement]

    def __init__(self, ast_node_class_overrides: dict[str, Type[Node]]) -> None:
        self.ast_node_class_overrides = ast_node_class_overrides

    def build(self) -> pp.ParserElement:
        """Build the grammar."""
        return pp.OneOrMore(self.g_codes() | self.m_codes() | self.d_codes())

    def d_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing D-codes."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> D01:
            parse_result_token_list = tokens.as_list()
            token_list = cast(list[Coordinate], parse_result_token_list)
            try:
                return self.get_cls(D01)(
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
            assert isinstance(value, str)
            assert value.startswith("D")
            assert len(value) > 1

            try:
                return self.get_cls(Dnn)(value=value)
            except ValidationError as e:
                raise pp.ParseFatalException(s, loc, "Invalid Dnn") from e

        dnn = pp.Regex(r"D0*[0-9]*").set_parse_action(_).set_name("Dnn")

        return d01 | d02 | d03 | dnn

    def get_cls(self, node_cls: Type[T]) -> Type[T]:
        """Get the class of the node."""
        return self.ast_node_class_overrides.get(node_cls.__qualname__, node_cls)

    @pp.cached_property
    def coordinate(self) -> pp.ParserElement:
        """Create a parser element capable of parsing coordinates."""

        def _(tokens: pp.ParseResults) -> Coordinate:
            type_, value = tokens.as_list()
            assert isinstance(type_, str), type(type_)
            assert type_ in ("X", "Y", "I", "J")
            assert isinstance(value, str)

            return self.get_cls(Coordinate)(type=type_, value=value)

        return (
            (
                pp.oneOf(("X", "Y", "I", "J")).set_name("coordinate_type")
                + pp.Regex(r"[+-]?[0-9]+").set_name("coordinate_value")
            )
            .set_parse_action(_)
            .set_name("coordinate")
        )

    def g_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing G-codes."""
        return pp.MatchFirst(
            [
                g(value, self.get_cls(cls))
                for (value, cls) in (
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
            ]
        )

    def m_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing M-codes."""
        return pp.MatchFirst(
            [
                m(value, self.get_cls(cls))
                for (value, cls) in (
                    (0, M00),
                    (1, M01),
                    (2, M02),
                )
            ]
        )


Grammar.DEFAULT = Grammar({}).build()
