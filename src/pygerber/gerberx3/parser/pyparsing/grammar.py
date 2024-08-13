"""`pygerber.gerberx3.parser.pyparsing.grammar` module contains the Gerber X3 grammar
implemented using the pyparsing library.
"""

from __future__ import annotations

from enum import IntFlag
from typing import Callable, ClassVar, List, Literal, Type, TypeVar, cast

import pyparsing as pp

from pygerber.gerberx3.ast.nodes.aperture.AB_close import ABclose
from pygerber.gerberx3.ast.nodes.aperture.AB_open import ABopen
from pygerber.gerberx3.ast.nodes.aperture.ADC import ADC
from pygerber.gerberx3.ast.nodes.aperture.ADmacro import ADmacro
from pygerber.gerberx3.ast.nodes.aperture.ADO import ADO
from pygerber.gerberx3.ast.nodes.aperture.ADP import ADP
from pygerber.gerberx3.ast.nodes.aperture.ADR import ADR
from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
from pygerber.gerberx3.ast.nodes.aperture.SR_open import SRopen
from pygerber.gerberx3.ast.nodes.attribute.TA import (
    AperFunction,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
)
from pygerber.gerberx3.ast.nodes.attribute.TD import TD
from pygerber.gerberx3.ast.nodes.attribute.TF import (
    TF_MD5,
    TF_CreationDate,
    TF_FileFunction,
    TF_FilePolarity,
    TF_GenerationSoftware,
    TF_Part,
    TF_ProjectId,
    TF_SameCoordinates,
    TF_UserName,
)
from pygerber.gerberx3.ast.nodes.attribute.TO import (
    TO_C,
    TO_CMNP,
    TO_N,
    TO_P,
    TO_CFtp,
    TO_CHgt,
    TO_CLbD,
    TO_CLbN,
    TO_CMfr,
    TO_CMnt,
    TO_CPgD,
    TO_CPgN,
    TO_CRot,
    TO_CSup,
    TO_CVal,
    TO_UserName,
)
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
from pygerber.gerberx3.ast.nodes.other.coordinate import (
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
)
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
from pygerber.gerberx3.ast.nodes.properties.FS import FS
from pygerber.gerberx3.ast.nodes.properties.IP import IP
from pygerber.gerberx3.ast.nodes.properties.IR import IR
from pygerber.gerberx3.ast.nodes.properties.MO import MO

T = TypeVar("T", bound=Node)


class Optimization(IntFlag):
    """Namespace class holding optimization level constants."""

    DISCARD_COMMENTS = 0b0000_0010
    DISCARD_ATTRIBUTES = 0b0000_0100


class Grammar:
    """Internal representation of the Gerber X3 grammar."""

    DEFAULT: ClassVar[pp.ParserElement]

    def __init__(
        self,
        ast_node_class_overrides: dict[str, Type[Node]],
        *,
        enable_packrat: bool = True,
        enable_debug: bool = False,
        optimization: int = 1,
    ) -> None:
        self.ast_node_class_overrides = ast_node_class_overrides
        self.enable_packrat = enable_packrat
        self.enable_debug = enable_debug
        self.optimization = optimization

    def build(self) -> pp.ParserElement:
        """Build the grammar."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> File:
            return self.get_cls(File)(source=s, location=loc, nodes=tokens.as_list())

        root = (
            pp.OneOrMore(
                pp.MatchFirst(
                    [
                        self.aperture(),
                        self.attribute(),
                        self.g_codes(),
                        self.m_codes(),
                        self.d_codes(),
                        self.properties(),
                    ]
                )
            )
            .set_results_name("root_node")
            .set_parse_action(_)
        )

        if self.enable_packrat:
            root.enable_packrat()

        if self.enable_debug:
            root.set_debug()

        return root

    @pp.cached_property
    def _asterisk(self) -> pp.ParserElement:
        return pp.Literal(r"*").set_name("*")

    @pp.cached_property
    def _extended(self) -> pp.ParserElement:
        return pp.Literal(r"%").set_name("%")

    def _command(self, inner: pp.ParserElement) -> pp.ParserElement:
        return inner + self._asterisk

    def _extended_command(self, inner: pp.ParserElement) -> pp.ParserElement:
        return self._extended + inner + self._asterisk + self._extended

    def get_cls(self, node_cls: Type[T]) -> Type[T]:
        """Get the class of the node."""
        return self.ast_node_class_overrides.get(node_cls.__qualname__, node_cls)  # type: ignore[return-value]

    @pp.cached_property
    def string(self) -> pp.ParserElement:
        """Create a parser element capable of parsing strings."""
        return pp.CharsNotIn("%*").set_results_name("string")

    @pp.cached_property
    def comma(self) -> pp.ParserElement:
        """Create a parser element capable of parsing commas."""
        return pp.Suppress(pp.Literal(",").set_name(","))

    @pp.cached_property
    def name(self) -> pp.ParserElement:
        """Create a parser element capable of parsing names."""
        return pp.Regex(r"[._a-zA-Z$][._a-zA-Z0-9]*").set_results_name("name")

    @pp.cached_property
    def user_name(self) -> pp.ParserElement:
        """Create a parser element capable of parsing user attribute names."""
        return pp.Regex(r"[_a-zA-Z$][._a-zA-Z0-9]*").set_results_name("user_name")

    @pp.cached_property
    def field(self) -> pp.ParserElement:
        """Create a parser element capable of parsing user attribute names."""
        return pp.Regex(r"[^%*,]*").set_results_name("field")

    @pp.cached_property
    def double(self) -> pp.ParserElement:
        """Create a parser element capable of parsing doubles."""
        return pp.Regex(r"[+-]?(([0-9]+(\.[0-9]+)?)|(\.[0-9]+))").set_results_name(
            "double"
        )

    @pp.cached_property
    def integer(self) -> pp.ParserElement:
        """Create a parser element capable of parsing integers."""
        return pp.Regex(r"[+-]?[0-9]+").set_results_name("integer")

    @pp.cached_property
    def aperture_identifier(self) -> pp.ParserElement:
        """Create a parser element capable of parsing aperture identifiers."""
        return pp.Regex(r"D[0]*[1-9][0-9]+").set_results_name("aperture_identifier")

    def make_unpack_callback(
        self, node_type: Type[Node]
    ) -> Callable[[str, int, pp.ParseResults], Node]:
        """Create a callback for unpacking the results of the parser."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> Node:
            return self.get_cls(node_type)(source=s, location=loc, **tokens.as_dict())

        return _

    #  █████  ██████  ███████ ██████  ████████ ██    ██ ██████  ███████
    # ██   ██ ██   ██ ██      ██   ██    ██    ██    ██ ██   ██ ██
    # ███████ ██████  █████   ██████     ██    ██    ██ ██████  █████
    # ██   ██ ██      ██      ██   ██    ██    ██    ██ ██   ██ ██
    # ██   ██ ██      ███████ ██   ██    ██     ██████  ██   ██ ███████

    def aperture(self) -> pp.ParserElement:
        """Create a parser element capable of parsing apertures."""
        return pp.MatchFirst(
            [
                self.aperture_block(),
                self.macro(),
                self.step_repeat(),
                self.add_aperture(),
            ]
        )

    def aperture_block(self) -> pp.ParserElement:
        """Create a parser element capable of parsing aperture blocks."""
        return pp.MatchFirst(
            [
                self.ab_open,
                self.ab_close,
            ]
        )

    @pp.cached_property
    def ab_open(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AB-open."""
        return (
            self._extended_command(pp.Literal("AB") + self.aperture_identifier)
            .set_name("ABopen")
            .set_parse_action(self.make_unpack_callback(ABopen))
        )

    @pp.cached_property
    def ab_close(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AB-close."""
        return (
            self._extended_command(pp.Literal("AB"))
            .set_name("ABclose")
            .set_parse_action(self.make_unpack_callback(ABclose))
        )

    def macro(self) -> pp.ParserElement:
        """Create a parser element capable of parsing macros."""
        return self.am_open + self.primitives + self.am_close

    @pp.cached_property
    def am_open(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AM-open."""
        return (
            (self._extended + pp.Literal("AM") + self.name + self._asterisk)
            .set_name("AMopen")
            .set_parse_action(self.make_unpack_callback(AMopen))
        )

    @pp.cached_property
    def am_close(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AM-close."""
        return self._extended.set_name("AM_close").set_parse_action(
            self.make_unpack_callback(AMclose)
        )

    def step_repeat(self) -> pp.ParserElement:
        """Create a parser element capable of parsing step repeats."""
        return pp.MatchFirst(
            [
                self.sr_open,
                self.sr_close,
            ]
        )

    @pp.cached_property
    def sr_open(self) -> pp.ParserElement:
        """Create a parser element capable of parsing SR-open."""
        return (
            self._extended_command(
                pp.Literal("SR")
                + pp.Opt(pp.Literal("X") + self.double.set_results_name("x"))
                + pp.Opt(pp.Literal("Y") + self.double.set_results_name("y"))
                + pp.Opt(pp.Literal("I") + self.double.set_results_name("i"))
                + pp.Opt(pp.Literal("J") + self.double.set_results_name("j"))
            )
            .set_name("SRopen")
            .set_parse_action(self.make_unpack_callback(SRopen))
        )

    @pp.cached_property
    def sr_close(self) -> pp.ParserElement:
        """Create a parser element capable of parsing SR-close."""
        return (
            self._extended_command(pp.Literal("SR"))
            .set_name("SRclose")
            .set_parse_action(self.make_unpack_callback(AMclose))
        )

    def add_aperture(self) -> pp.ParserElement:
        """Create a parser element capable of parsing add-aperture commands."""
        return pp.MatchFirst(
            [
                self.add_aperture_circle(),
                self.add_aperture_rectangle("R", ADR),
                self.add_aperture_rectangle("O", ADO),
                self.add_aperture_polygon(),
                self.add_aperture_macro(),
            ]
        )

    def add_aperture_circle(self) -> pp.ParserElement:
        """Create a parser element capable of parsing add-aperture-circle commands."""
        return (
            self._extended_command(
                pp.Literal("AD")
                + self.aperture_identifier
                + pp.Literal("C,")
                + self.double.set_results_name("diameter")
                + pp.Opt(self._x + self.double.set_results_name("hole_diameter"))
            )
            .set_name("ADC")
            .set_parse_action(self.make_unpack_callback(ADC))
        )

    def add_aperture_rectangle(
        self, symbol: Literal["R", "O"], cls: Type[Node]
    ) -> pp.ParserElement:
        """Create a parser element capable of parsing add-aperture-rectangle
        commands.
        """
        return (
            self._extended_command(
                pp.Literal("AD")
                + self.aperture_identifier
                + pp.Literal(f"{symbol},")
                + self.double.set_results_name("width")
                + self._x
                + self.double.set_results_name("height")
                + pp.Opt(self._x + self.double.set_results_name("hole_diameter"))
            )
            .set_name(f"AD{symbol}")
            .set_parse_action(self.make_unpack_callback(cls))
        )

    def add_aperture_polygon(self) -> pp.ParserElement:
        """Create a parser element capable of parsing add-aperture-polygon
        commands.
        """
        return (
            self._extended_command(
                pp.Literal("AD")
                + self.aperture_identifier
                + pp.Literal("P,")
                + self.double.set_results_name("outer_diameter")
                + self._x
                + self.double.set_results_name("vertices")
                + pp.Opt(self._x + self.double.set_results_name("rotation"))
                + pp.Opt(self._x + self.double.set_results_name("hole_diameter"))
            )
            .set_name("ADP")
            .set_parse_action(self.make_unpack_callback(ADP))
        )

    def add_aperture_macro(self) -> pp.ParserElement:
        """Create a parser element capable of parsing add-aperture-polygon
        commands.
        """
        param = self.double.set_results_name("params", list_all_matches=True)

        return (
            self._extended_command(
                pp.Literal("AD")
                + self.aperture_identifier
                + self.name.set_results_name("name")
                + pp.Opt(self.comma + param + pp.ZeroOrMore(self._x + param))
            )
            .set_name("ADmacro")
            .set_parse_action(self.make_unpack_callback(ADmacro))
        )

    @pp.cached_property
    def _x(self) -> pp.ParserElement:
        return pp.Suppress(pp.Literal("X")).set_name("X")

    #  █████  ████████ ████████ ██████  ██ ██████  ██    ██ ████████ ███████
    # ██   ██    ██       ██    ██   ██ ██ ██   ██ ██    ██    ██    ██
    # ███████    ██       ██    ██████  ██ ██████  ██    ██    ██    █████
    # ██   ██    ██       ██    ██   ██ ██ ██   ██ ██    ██    ██    ██
    # ██   ██    ██       ██    ██   ██ ██ ██████   ██████     ██    ███████

    def attribute(self) -> pp.ParserElement:
        """Create a parser element capable of parsing attributes."""
        return pp.MatchFirst(
            [
                self.ta(),
                self.td(),
                self.tf(),
                self.to(),
            ]
        )

    def ta(self) -> pp.ParserElement:
        """Create a parser element capable of parsing TA attributes."""
        return pp.MatchFirst(
            [
                self._ta_user_name,
                self._ta_aper_function,
                self._ta_drill_tolerance,
                self._ta_flash_text,
            ]
        )

    @pp.cached_property
    def _ta_user_name(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._ta
                + self.user_name
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TA<UserName>")
            .set_parse_action(self.make_unpack_callback(TA_UserName))
        )

    @pp.cached_property
    def _ta_aper_function(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._ta
                + pp.Literal(".AperFunction")
                + pp.Optional(
                    self.comma
                    + pp.one_of([v.value for v in AperFunction]).set_results_name(
                        "function"
                    )
                )
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TA.AperFunction")
            .set_parse_action(self.make_unpack_callback(TA_AperFunction))
        )

    @pp.cached_property
    def _ta_drill_tolerance(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._ta
                + pp.Literal(".DrillTolerance")
                + pp.Optional(
                    self.comma
                    + self.double.set_results_name("plus_tolerance")
                    + pp.Optional(
                        self.comma + self.double.set_results_name("minus_tolerance")
                    )
                )
            )
            .set_name("TA.DrillTolerance")
            .set_parse_action(self.make_unpack_callback(TA_DrillTolerance))
        )

    @pp.cached_property
    def _ta_flash_text(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._ta
                + pp.Literal(".FlashText")
                + self.comma
                + self.field.set_results_name("string")
                + self.comma
                + pp.one_of(list("BC")).set_results_name("mode")
                + self.comma
                + pp.Opt(pp.one_of(list("RM")).set_results_name("mirroring"))
                + self.comma
                + pp.Opt(self.field.set_results_name("font"))
                + self.comma
                + pp.Opt(self.field.set_results_name("size"))
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("comments", list_all_matches=True)
                )
            )
            .set_name("TA.FlashText")
            .set_parse_action(self.make_unpack_callback(TA_FlashText))
        )

    @pp.cached_property
    def _ta(self) -> pp.ParserElement:
        return pp.Literal("TA")

    def td(self) -> pp.ParserElement:
        """Create a parser element capable of parsing TD attributes."""
        return (
            self._extended_command(
                pp.Literal("TD") + pp.Opt(self.string.set_results_name("name"))
            )
            .set_name("TD")
            .set_parse_action(self.make_unpack_callback(TD))
        )

    def tf(self) -> pp.ParserElement:
        """Create a parser element capable of parsing TF attributes."""
        return pp.MatchFirst(
            [
                self._tf_user_name,
                self._tf_part,
                self._tf_file_function,
                self._tf_file_polarity,
                self._tf_same_coordinates,
                self._tf_creation_date,
                self._tf_generation_software,
                self._tf_project_id,
                self._tf_md5,
            ]
        )

    @pp.cached_property
    def _tf_user_name(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + self.user_name
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TF<UserName>")
            .set_parse_action(self.make_unpack_callback(TF_UserName))
        )

    @pp.cached_property
    def _tf_part(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".Part")
                + self.comma
                + self.field.set_results_name("part")
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TF.Part")
            .set_parse_action(self.make_unpack_callback(TF_Part))
        )

    @pp.cached_property
    def _tf_file_function(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".FileFunction")
                + self.comma
                + self.field.set_results_name("file_function")
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TF.FileFunction")
            .set_parse_action(self.make_unpack_callback(TF_FileFunction))
        )

    @pp.cached_property
    def _tf_file_polarity(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".FilePolarity")
                + self.comma
                + self.field.set_results_name("polarity")
            )
            .set_name("TF.FilePolarity")
            .set_parse_action(self.make_unpack_callback(TF_FilePolarity))
        )

    @pp.cached_property
    def _tf_same_coordinates(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".SameCoordinates")
                + pp.Opt(self.comma + self.field.set_results_name("identifier"))
            )
            .set_name("TF.SameCoordinates")
            .set_parse_action(self.make_unpack_callback(TF_SameCoordinates))
        )

    @pp.cached_property
    def _tf_creation_date(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".CreationDate")
                + self.comma
                + self.field.set_results_name("creation_date")
            )
            .set_name("TF.CreationDate")
            .set_parse_action(self.make_unpack_callback(TF_CreationDate))
        )

    @pp.cached_property
    def _tf_generation_software(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".GenerationSoftware")
                + pp.Opt(
                    self.comma
                    + self.field.set_results_name("vendor")
                    + pp.Opt(
                        self.comma
                        + self.field.set_results_name("application")
                        + pp.Opt(self.comma + self.field.set_results_name("version"))
                    )
                )
            )
            .set_name("TF.GenerationSoftware")
            .set_parse_action(self.make_unpack_callback(TF_GenerationSoftware))
        )

    @pp.cached_property
    def _tf_project_id(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".ProjectId")
                + pp.Opt(
                    self.comma
                    + self.field.set_results_name("name")
                    + pp.Opt(
                        self.comma
                        + self.field.set_results_name("guid")
                        + pp.Opt(self.comma + self.field.set_results_name("revision"))
                    )
                )
            )
            .set_name("TF.ProjectId")
            .set_parse_action(self.make_unpack_callback(TF_ProjectId))
        )

    @pp.cached_property
    def _tf_md5(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._tf
                + pp.CaselessLiteral(".MD5")
                + self.comma
                + self.field.set_results_name("md5")
            )
            .set_name("TF.MD5")
            .set_parse_action(self.make_unpack_callback(TF_MD5))
        )

    @pp.cached_property
    def _tf(self) -> pp.ParserElement:
        return pp.Literal("TF")

    def to(self) -> pp.ParserElement:
        """Create a parser element capable of parsing TO attributes."""
        return pp.MatchFirst(
            [
                self._to_user_name,
                self._to_n,
                self._to_p,
                self._to_c,
                self._to_crot,
                self._to_cmfr,
                self._to_cmpn,
                self._to_cval,
                self._to_cmnt,
                self._to_cftp,
                self._to_cpgn,
                self._to_cpgd,
                self._to_chgt,
                self._to_clbn,
                self._to_clbd,
                self._to_csup,
            ]
        )

    @pp.cached_property
    def _to_user_name(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + self.user_name
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("fields", list_all_matches=True)
                )
            )
            .set_name("TO<UserName>")
            .set_parse_action(self.make_unpack_callback(TO_UserName))
        )

    @pp.cached_property
    def _to_n(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".N")
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name("net_names", list_all_matches=True)
                )
            )
            .set_name("TO.N")
            .set_parse_action(self.make_unpack_callback(TO_N))
        )

    @pp.cached_property
    def _to_p(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".P")
                + self.comma
                + self.field.set_results_name("refdes")
                + self.comma
                + self.field.set_results_name("number")
                + pp.Opt(self.comma + self.field.set_results_name("function"))
            )
            .set_name("TO.P")
            .set_parse_action(self.make_unpack_callback(TO_P))
        )

    @pp.cached_property
    def _to_c(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".C")
                + self.comma
                + self.field.set_results_name("refdes")
            )
            .set_name("TO.C")
            .set_parse_action(self.make_unpack_callback(TO_C))
        )

    @pp.cached_property
    def _to_crot(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CRot")
                + self.comma
                + self.field.set_results_name("angle")
            )
            .set_name("TO.CRot")
            .set_parse_action(self.make_unpack_callback(TO_CRot))
        )

    @pp.cached_property
    def _to_cmfr(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CMfr")
                + self.comma
                + self.field.set_results_name("manufacturer")
            )
            .set_name("TO.CMfr")
            .set_parse_action(self.make_unpack_callback(TO_CMfr))
        )

    @pp.cached_property
    def _to_cmpn(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CMPN")
                + self.comma
                + self.field.set_results_name("part_number")
            )
            .set_name("TO.CMPN")
            .set_parse_action(self.make_unpack_callback(TO_CMNP))
        )

    @pp.cached_property
    def _to_cval(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CVal")
                + self.comma
                + self.field.set_results_name("value")
            )
            .set_name("TO.CVal")
            .set_parse_action(self.make_unpack_callback(TO_CVal))
        )

    @pp.cached_property
    def _to_cmnt(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CMnt")
                + self.comma
                + self.field.set_results_name("mount")
            )
            .set_name("TO.CMnt")
            .set_parse_action(self.make_unpack_callback(TO_CMnt))
        )

    @pp.cached_property
    def _to_cftp(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CFtp")
                + self.comma
                + self.field.set_results_name("footprint")
            )
            .set_name("TO.CFtp")
            .set_parse_action(self.make_unpack_callback(TO_CFtp))
        )

    @pp.cached_property
    def _to_cpgn(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CPgN")
                + self.comma
                + self.field.set_results_name("name")
            )
            .set_name("TO.CPgN")
            .set_parse_action(self.make_unpack_callback(TO_CPgN))
        )

    @pp.cached_property
    def _to_cpgd(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CPgD")
                + self.comma
                + self.field.set_results_name("description")
            )
            .set_name("TO.CPgD")
            .set_parse_action(self.make_unpack_callback(TO_CPgD))
        )

    @pp.cached_property
    def _to_chgt(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CHgt")
                + self.comma
                + self.field.set_results_name("height")
            )
            .set_name("TO.CHgt")
            .set_parse_action(self.make_unpack_callback(TO_CHgt))
        )

    @pp.cached_property
    def _to_clbn(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CLbn")
                + self.comma
                + self.field.set_results_name("name")
            )
            .set_name("TO.CLbn")
            .set_parse_action(self.make_unpack_callback(TO_CLbN))
        )

    @pp.cached_property
    def _to_clbd(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CLbD")
                + self.comma
                + self.field.set_results_name("description")
            )
            .set_name("TO.CLbD")
            .set_parse_action(self.make_unpack_callback(TO_CLbD))
        )

    @pp.cached_property
    def _to_csup(self) -> pp.ParserElement:
        return (
            self._extended_command(
                self._to
                + pp.CaselessLiteral(".CSup")
                + self.comma
                + self.field.set_results_name("supplier")
                + self.comma
                + self.field.set_results_name("supplier_part")
                + pp.ZeroOrMore(
                    self.comma
                    + self.field.set_results_name(
                        "other_suppliers", list_all_matches=True
                    )
                )
            )
            .set_name("TO.CSup")
            .set_parse_action(self.make_unpack_callback(TO_CSup))
        )

    @pp.cached_property
    def _to(self) -> pp.ParserElement:
        return pp.Literal("TO")

    # ██████      █████ ███████ ██████  ███████ ███████
    # ██   ██    ██     ██   ██ ██   ██ ██      ██
    # ██   ██    ██     ██   ██ ██   ██ █████   ███████
    # ██   ██    ██     ██   ██ ██   ██ ██           ██
    # ██████      █████ ███████ ██████  ███████ ███████

    def d_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing D-codes."""
        return pp.MatchFirst(
            [
                self._dnn,
                self._d01,
                self._d02,
                self._d03,
            ]
        )

    @pp.cached_property
    def _dnn(self) -> pp.ParserElement:
        return (
            self._command(self.aperture_identifier.set_results_name("value"))
            .set_parse_action(self.make_unpack_callback(Dnn))
            .set_name("Dnn")
        )

    @pp.cached_property
    def _d01(self) -> pp.ParserElement:
        return (
            self._command(
                pp.Opt(self._coordinate_x.set_results_name("x"))
                + pp.Opt(self._coordinate_y.set_results_name("y"))
                + pp.Opt(self._coordinate_i.set_results_name("i"))
                + pp.Opt(self._coordinate_j.set_results_name("j"))
                + pp.Regex(r"D0*1")
            )
            .set_parse_action(self.make_unpack_callback(D01))
            .set_name("D01")
        )

    @pp.cached_property
    def _d02(self) -> pp.ParserElement:
        return (
            self._command(
                self._coordinate_x.set_results_name("x")
                + self._coordinate_y.set_results_name("y")
                + pp.Regex(r"D0*2")
            )
            .set_parse_action(self.make_unpack_callback(D02))
            .set_name("D02")
        )

    @pp.cached_property
    def _d03(self) -> pp.ParserElement:
        return (
            self._command(
                pp.Opt(self._coordinate_x.set_results_name("x"))
                + pp.Opt(self._coordinate_y.set_results_name("y"))
                + pp.Regex(r"D0*3")
            )
            .set_parse_action(self.make_unpack_callback(D03))
            .set_name("D03")
        )

    #  ██████      █████ ███████ ██████  ███████ ███████
    # ██          ██     ██   ██ ██   ██ ██      ██
    # ██   ███    ██     ██   ██ ██   ██ █████   ███████
    # ██    ██    ██     ██   ██ ██   ██ ██           ██
    #  ██████      █████ ███████ ██████  ███████ ███████

    def g_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing G-codes."""
        g04_comment = self._command(
            pp.Regex(r"G0*4") + pp.Opt(self.string),
        ).set_name("G04")

        if self.optimization & Optimization.DISCARD_COMMENTS:
            g04_comment = pp.Suppress(g04_comment)
        else:
            g04_comment = g04_comment.set_parse_action(self.make_unpack_callback(G04))

        g54 = (
            (pp.Regex(r"G0*54") + self._dnn.set_results_name("dnn"))
            .set_name("G54")
            .set_parse_action(self.make_unpack_callback(G54))
        )
        g55 = (
            (pp.Regex(r"G0*55") + self._d03.set_results_name("flash"))
            .set_name("G55")
            .set_parse_action(self.make_unpack_callback(G55))
        )
        return pp.MatchFirst(
            [
                g04_comment,
                g54,
                g55,
                *(
                    self.g(
                        value,
                        self.get_cls(cls),  # type: ignore[arg-type, type-abstract]
                    )
                    for (value, cls) in reversed(
                        (
                            (1, G01),
                            (2, G02),
                            (3, G03),
                            (36, G36),
                            (37, G37),
                            (54, G54),
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

    def g(self, value: int, cls: Type[Node]) -> pp.ParserElement:
        """Create a parser element capable of parsing particular G-code."""
        return (
            self._command(pp.Regex(r"G0*" + str(value)))
            .set_name(f"G{value}")
            .set_parse_action(self.make_unpack_callback(cls))
        )

    # ██      ██████   █████  ██████      █████ ███████ ███    ███ ███    ███  █████  ███    ██ ██████  ███████ # noqa: E501
    # ██     ██    ██ ██   ██ ██   ██    ██     ██   ██ ████  ████ ████  ████ ██   ██ ████   ██ ██   ██ ██      # noqa: E501
    # ██     ██    ██ ███████ ██   ██    ██     ██   ██ ██ ████ ██ ██ ████ ██ ███████ ██ ██  ██ ██   ██ ███████ # noqa: E501
    # ██     ██    ██ ██   ██ ██   ██    ██     ██   ██ ██  ██  ██ ██  ██  ██ ██   ██ ██  ██ ██ ██   ██      ██ # noqa: E501
    # ██████ ███████  ██   ██ ██████      █████ ███████ ██      ██ ██      ██ ██   ██ ██   ████ ██████  ███████ # noqa: E501

    # ███    ███     █████ ███████ ██████  ███████ ███████
    # ████  ████    ██     ██   ██ ██   ██ ██      ██
    # ██ ████ ██    ██     ██   ██ ██   ██ █████   ███████
    # ██  ██  ██    ██     ██   ██ ██   ██ ██           ██
    # ██      ██     █████ ███████ ██████  ███████ ███████

    def m_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing M-codes."""
        return pp.MatchFirst(
            [
                self.m(
                    value,
                    self.get_cls(cls),  # type: ignore[arg-type, type-abstract]
                )
                for (value, cls) in (
                    (2, M02),
                    (1, M01),
                    (0, M00),
                )
            ]
        )

    def m(self, value: int, cls: Type[Node]) -> pp.ParserElement:
        """Create a parser element capable of parsing particular D-code."""
        return (
            self._command(pp.Regex(r"M0*" + str(value)))
            .set_name(f"M{value}")
            .set_parse_action(self.make_unpack_callback(cls))
        )

    # ███    ███  █████  ████████ ██   ██
    # ████  ████ ██   ██    ██    ██   ██
    # ██ ████ ██ ███████    ██    ███████
    # ██  ██  ██ ██   ██    ██    ██   ██
    # ██      ██ ██   ██    ██    ██   ██

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
                    pp.Suppress(pp.one_of("x X")),
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
        return self.double.set_results_name("constant").set_parse_action(
            self.make_unpack_callback(Constant)
        )

    @pp.cached_property
    def variable(self) -> pp.ParserElement:
        """Create a parser element capable of parsing variables."""
        return (
            pp.Regex(r"\$[0-9]+")
            .set_results_name("variable")
            .set_parse_action(self.make_unpack_callback(Variable))
        )

    @pp.cached_property
    def assignment(self) -> pp.ParserElement:
        """Create a parser element capable of parsing assignments."""
        return (
            self._command(
                self.variable
                + pp.Suppress("=")
                + self.expression.set_results_name("expression")
            )
            .set_results_name("assignment")
            .set_parse_action(self.make_unpack_callback(Assignment))
        )

    #  ██████ ████████ ██   ██ ███████ ██████
    # ██    ██   ██    ██   ██ ██      ██   ██
    # ██    ██   ██    ███████ █████   ██████
    # ██    ██   ██    ██   ██ ██      ██   ██
    #  ██████    ██    ██   ██ ███████ ██   ██

    @pp.cached_property
    def _coordinate_x(self) -> pp.ParserElement:
        return (
            (pp.CaselessLiteral("X") + self.integer.set_results_name("value"))
            .set_parse_action(self.make_unpack_callback(CoordinateX))
            .set_name("coordinate.x")
        )

    @pp.cached_property
    def _coordinate_y(self) -> pp.ParserElement:
        return (
            (pp.CaselessLiteral("Y") + self.integer.set_results_name("value"))
            .set_parse_action(self.make_unpack_callback(CoordinateY))
            .set_name("coordinate.y")
        )

    @pp.cached_property
    def _coordinate_i(self) -> pp.ParserElement:
        return (
            (pp.CaselessLiteral("I") + self.integer.set_results_name("value"))
            .set_parse_action(self.make_unpack_callback(CoordinateI))
            .set_name("coordinate.i")
        )

    @pp.cached_property
    def _coordinate_j(self) -> pp.ParserElement:
        return (
            (pp.CaselessLiteral("J") + self.integer.set_results_name("value"))
            .set_parse_action(self.make_unpack_callback(CoordinateJ))
            .set_name("coordinate.j")
        )

    # ██████  ██████  ██ ███    ███ ██ ████████ ██ ██    ██ ███████ ███████
    # ██   ██ ██   ██ ██ ████  ████ ██    ██    ██ ██    ██ ██      ██
    # ██████  ██████  ██ ██ ████ ██ ██    ██    ██ ██    ██ █████   ███████
    # ██      ██   ██ ██ ██  ██  ██ ██    ██    ██  ██  ██  ██           ██
    # ██      ██   ██ ██ ██      ██ ██    ██    ██   ████   ███████ ███████

    @pp.cached_property
    def primitives(self) -> pp.ParserElement:
        """Create a parser element capable of parsing macro primitives."""
        cs = self.comma

        return pp.ZeroOrMore(
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
                            .set_parse_action(self.make_unpack_callback(Point)),
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

    def primitive(
        self, cls: Type[Node], code: int, fields: pp.ParserElement
    ) -> pp.ParserElement:
        """Create a parser element capable of parsing a primitive."""
        return (
            self._command(pp.Literal(str(code)) + fields)
            .set_name(f"primitive-{code}")
            .set_parse_action(self.make_unpack_callback(cls))
        )

    # ██████  ██████   ██████  ██████  ███████ ███████ ███████ ██ ███████ ███████
    # ██   ██ ██   ██ ██    ██ ██   ██ ██      ██   ██   ██    ██ ██      ██
    # ██████  ██████  ██    ██ ██████  █████   ██████    ██    ██ █████   ███████
    # ██      ██   ██ ██    ██ ██      ██      ██   ██   ██    ██ ██           ██
    # ██      ██   ██  ██████  ██      ███████ ██   ██   ██    ██ ███████ ███████

    def properties(self) -> pp.ParserElement:
        """Create a parser element capable of parsing Properties-commands."""
        return pp.MatchFirst([self.fs(), self.mo(), self.ip(), self.ir()])

    def fs(self) -> pp.ParserElement:
        """Create a parser for the FS command."""
        return (
            self._extended_command(
                pp.Literal("FS")
                + pp.one_of(("L", "T")).set_results_name("zeros")
                + pp.one_of(("I", "A")).set_results_name("coordinate_mode")
                + pp.CaselessLiteral("X")
                + pp.Regex(r"[0-9]").set_results_name("x_integral")
                + pp.Regex(r"[0-9]").set_results_name("x_decimal")
                + pp.CaselessLiteral("Y")
                + pp.Regex(r"[0-9]").set_results_name("y_integral")
                + pp.Regex(r"[0-9]").set_results_name("y_decimal")
            )
            .set_parse_action(self.make_unpack_callback(FS))
            .set_name("FS")
        )

    def ip(self) -> pp.ParserElement:
        """Create a parser for the IP command."""
        return (
            self._extended_command(
                pp.Literal("IP")
                + pp.one_of(("POS", "NEG")).set_results_name("polarity")
            )
            .set_parse_action(self.make_unpack_callback(IP))
            .set_name("IP")
        )

    def ir(self) -> pp.ParserElement:
        """Create a parser for the IR command."""
        return (
            self._extended_command(
                pp.Literal("IR") + self.double.set_results_name("rotation_degrees")
            )
            .set_parse_action(self.make_unpack_callback(IR))
            .set_name("IR")
        )

    def mo(self) -> pp.ParserElement:
        """Create a parser for the MO command."""
        return (
            self._extended_command(
                pp.Literal("MO") + pp.one_of(["IN", "MM"]).set_results_name("mode")
            )
            .set_parse_action(self.make_unpack_callback(MO))
            .set_name("MO")
        )


Grammar.DEFAULT = Grammar({}).build()
