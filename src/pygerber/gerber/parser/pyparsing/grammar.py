"""The `grammar` module contains the Gerber X3 grammar implemented using the pyparsing
library.
"""

from __future__ import annotations

from enum import IntFlag
from typing import Any, Callable, Iterable, Literal, Optional, Type, TypeVar, cast

import pyparsing as pp
from pydantic import BaseModel

from pygerber.gerber.ast.nodes import (
    AB,
    ADC,
    ADO,
    ADP,
    ADR,
    AM,
    AS,
    D01,
    D02,
    D03,
    FS,
    G01,
    G02,
    G03,
    G04,
    G36,
    G37,
    G54,
    G55,
    G70,
    G71,
    G74,
    G75,
    G90,
    G91,
    IN,
    IP,
    IR,
    LM,
    LN,
    LP,
    LR,
    LS,
    M00,
    M01,
    M02,
    MI,
    MO,
    OF,
    SF,
    SR,
    TD,
    TF_MD5,
    TO_C,
    TO_CMNP,
    TO_N,
    TO_P,
    ABclose,
    ABopen,
    Add,
    ADmacro,
    AMclose,
    AMopen,
    Assignment,
    Code0,
    Code1,
    Code2,
    Code4,
    Code5,
    Code6,
    Code7,
    Code20,
    Code21,
    Code22,
    Constant,
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
    Div,
    Dnn,
    File,
    Invalid,
    Mul,
    Neg,
    Node,
    Parenthesis,
    Point,
    Pos,
    SourceInfo,
    SRclose,
    SRopen,
    Sub,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
    TF_CreationDate,
    TF_FileFunction,
    TF_FilePolarity,
    TF_GenerationSoftware,
    TF_Part,
    TF_ProjectId,
    TF_SameCoordinates,
    TF_UserName,
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
    Variable,
)
from pygerber.gerber.ast.nodes.enums import AperFunction

T = TypeVar("T", bound=Node)


class Optimization(IntFlag):
    """Namespace class holding optimization level constants."""

    DISCARD_COMMENTS = 0b0000_0010
    DISCARD_ATTRIBUTES = 0b0000_0100


class SyntaxSwitches(BaseModel):
    """The `SyntaxSwitches` class contains switches for toggling support for different
    variants of Gerber derived grammars not compatible with Gerber X3.
    """

    allow_d01_without_code: bool = True
    """Allow D01 commands with `D01` literal omitted.

    Example:
    --------

    ```gerber
    X2331205Y10807331I4J-31018*
    ```

    """

    allow_non_standalone_d_codes: bool = True
    """Allow G codes merged with D codes.

    Example:
    --------

    ```gerber
    G01X2241001Y10806845D02*
    ```

    """


class Grammar:
    """Internal representation of the Gerber X3 grammar."""

    def __init__(
        self,
        ast_node_class_overrides: dict[str, Type[Node]],
        syntax_switches: Optional[SyntaxSwitches] = None,
        *,
        enable_packrat: bool = False,
        packrat_cache_size: int = 128,
        enable_debug: bool = False,
        optimization: int = 0,
    ) -> None:
        self.ast_node_class_overrides = ast_node_class_overrides
        self.syntax_switches = syntax_switches or SyntaxSwitches()

        self.enable_packrat = enable_packrat
        self.packrat_cache_size = packrat_cache_size
        self.enable_debug = enable_debug
        self.optimization = optimization

        self.step_repeat_forward = pp.Forward()
        self.aperture_block_forward = pp.Forward()

    def build(self) -> pp.ParserElement:
        """Build the grammar."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> File:
            return self.get_cls(File)(
                source_info=SourceInfo(source=s, location=loc, length=len(s) - loc),
                nodes=tokens.as_list(),
            )

        root = (
            pp.OneOrMore(
                pp.MatchFirst(
                    [
                        self.d_codes_standalone,
                        self.g_codes,
                        self.load_commands,
                        self.aperture(),
                        self.attribute,
                        self.properties,
                        self.m_codes,
                    ]
                )
            )
            .set_results_name("root_node")
            .set_parse_action(_)
        )

        if self.enable_packrat:
            root.enable_packrat(cache_size_limit=self.packrat_cache_size)

        if self.enable_debug:
            root.set_debug()

        return root

    def build_resilient(self) -> pp.ParserElement:
        """Build the grammar."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> File:
            return self.get_cls(File)(
                source_info=SourceInfo(source=s, location=loc, length=len(s) - loc),
                nodes=tokens.as_list(),
            )

        root = (
            pp.OneOrMore(
                pp.MatchFirst(
                    [
                        self.d_codes_standalone,
                        self.g_codes,
                        self.load_commands,
                        self.aperture(),
                        self.attribute,
                        self.properties,
                        self.m_codes,
                        self._invalid_token,
                    ]
                )
            )
            .set_results_name("root_node")
            .set_parse_action(_)
        )

        if self.enable_packrat:
            root.enable_packrat(cache_size_limit=self.packrat_cache_size)

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
        return pp.Literal(",").set_name(",")

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
    def boolean(self) -> pp.ParserElement:
        """Create a parser element capable of parsing integers."""
        return pp.one_of(("0", "1")).set_results_name("boolean")

    @pp.cached_property
    def aperture_id(self) -> pp.ParserElement:
        """Create a parser element capable of parsing aperture identifiers."""
        return pp.Regex(r"D[0]*[1-9][0-9]+").set_results_name("aperture_id")

    def make_unpack_callback(
        self,
        node_type: Type[Node],
        **kwargs: Any,
    ) -> Callable[[str, int, pp.ParseResults], Node]:
        """Create a callback for unpacking the results of the parser."""

        def _(s: str, loc: int, tokens: pp.ParseResults) -> Node:
            return self.get_cls(node_type)(
                source_info=SourceInfo(
                    source=s, location=loc, length=sum(len(t) for t in tokens.as_list())
                ),
                **tokens.as_dict(),
                **kwargs,
            )

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
                self.aperture_block,
                self.macro,
                self.step_repeat,
                self.add_aperture,
            ]
        )

    @pp.cached_property
    def aperture_block(self) -> pp.ParserElement:
        """Create a parser element capable of parsing aperture blocks."""
        self.aperture_block_forward = pp.Forward()

        self.aperture_block_forward <<= (
            (
                self.ab_open.set_results_name("open")
                + pp.ZeroOrMore(
                    pp.MatchFirst(
                        [
                            self.d_codes_standalone,
                            self.g_codes,
                            self.load_commands,
                            self.properties,
                            self.attribute,
                            self.add_aperture,
                            self.step_repeat_forward,
                            self.aperture_block_forward,
                            self.macro,
                            # Technically not valid according to standard.
                            self.m_codes,
                        ]
                    )
                ).set_results_name("nodes")
                + self.ab_close.set_results_name("close")
            )
            .set_name("ApertureBlock")
            .set_parse_action(self.make_unpack_callback(AB))
        )

        return self.aperture_block_forward

    @pp.cached_property
    def ab_open(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AB-open."""
        return (
            self._extended_command(pp.Literal("AB") + self.aperture_id)
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

    @pp.cached_property
    def macro(self) -> pp.ParserElement:
        """Create a parser element capable of parsing macros."""
        return (
            (
                self.am_open.set_results_name("open")
                + self.primitives.set_results_name("primitives")
                + self.am_close.set_results_name("close")
            )
            .set_name("MacroDefinition")
            .set_parse_action(self.make_unpack_callback(AM))
        )

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
        return (
            self._extended.copy()
            .set_name("AM_close")
            .set_parse_action(self.make_unpack_callback(AMclose))
        )

    @pp.cached_property
    def step_repeat(self) -> pp.ParserElement:
        """Create a parser element capable of parsing step repeats."""
        self.step_and_repeat_block_forward = pp.Forward()

        self.step_and_repeat_block_forward <<= (
            (
                self.sr_open.set_results_name("open")
                + pp.ZeroOrMore(
                    pp.MatchFirst(
                        [
                            self.d_codes_standalone,
                            self.g_codes,
                            self.load_commands,
                            self.properties,
                            self.attribute,
                            self.add_aperture,
                            self.step_repeat_forward,
                            self.aperture_block_forward,
                            self.macro,
                            # Technically not valid according to standard.
                            self.m_codes,
                        ]
                    )
                ).set_results_name("nodes")
                + self.sr_close.set_results_name("close")
            )
            .set_name("StepAndRepeatBlock")
            .set_parse_action(self.make_unpack_callback(SR))
        )

        return self.step_and_repeat_block_forward

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
            .set_parse_action(self.make_unpack_callback(SRclose))
        )

    @pp.cached_property
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
                + self.aperture_id
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
                + self.aperture_id
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
                + self.aperture_id
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
                + self.aperture_id
                + self.name.set_results_name("name")
                + pp.Opt(self.comma + param + pp.ZeroOrMore(self._x + param))
            )
            .set_name("ADmacro")
            .set_parse_action(self.make_unpack_callback(ADmacro))
        )

    @pp.cached_property
    def _x(self) -> pp.ParserElement:
        return pp.Literal("X").set_name("X")

    #  █████  ████████ ████████ ██████  ██ ██████  ██    ██ ████████ ███████
    # ██   ██    ██       ██    ██   ██ ██ ██   ██ ██    ██    ██    ██
    # ███████    ██       ██    ██████  ██ ██████  ██    ██    ██    █████
    # ██   ██    ██       ██    ██   ██ ██ ██   ██ ██    ██    ██    ██
    # ██   ██    ██       ██    ██   ██ ██ ██████   ██████     ██    ███████

    @pp.cached_property
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
                + pp.Opt(self.field).set_results_name("font")
                + self.comma
                + pp.Opt(self.field).set_results_name("size")
                + pp.ZeroOrMore(
                    self.comma
                    + pp.Opt(self.field).set_results_name(
                        "comments", list_all_matches=True
                    )
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

    @pp.cached_property
    def d_codes_standalone(self) -> pp.ParserElement:
        """Create a parser element capable of parsing standalone D-codes."""
        return self._d_codes(is_standalone=True)

    @pp.cached_property
    def d_codes_non_standalone(self) -> pp.ParserElement:
        """Create a parser element capable of parsing standalone D-codes."""
        return self._d_codes(is_standalone=False)

    def _d_codes(self, *, is_standalone: bool) -> pp.ParserElement:
        """Create a parser element capable of parsing D-codes.

        `is_standalone` parameter is used to determine if the D-code is standalone, ie.
        not prefixed by a G-code with no asterisk at the end. See `D.is_standalone` or
        `G.is_standalone` for more information.
        """
        return pp.MatchFirst(
            [
                self._dnn(is_standalone=is_standalone),
                self._d01(is_standalone=is_standalone),
                self._d02(is_standalone=is_standalone),
                self._d03(is_standalone=is_standalone),
            ]
        )

    def _dnn(self, *, is_standalone: bool) -> pp.ParserElement:
        return (
            self._command(self.aperture_id.set_results_name("aperture_id"))
            .set_parse_action(
                self.make_unpack_callback(Dnn, is_standalone=is_standalone)
            )
            .set_name("Dnn")
        )

    def _d01(self, *, is_standalone: bool) -> pp.ParserElement:
        regex_d01: pp.ParserElement = pp.Regex(r"D0*1")
        if self.syntax_switches.allow_d01_without_code:
            regex_d01 = pp.Opt(regex_d01)

        return (
            self._command(
                pp.Opt(self._coordinate_x.set_results_name("x"))
                + pp.Opt(self._coordinate_y.set_results_name("y"))
                + pp.Opt(self._coordinate_i.set_results_name("i"))
                + pp.Opt(self._coordinate_j.set_results_name("j"))
                + regex_d01
            )
            .set_parse_action(
                self.make_unpack_callback(D01, is_standalone=is_standalone)
            )
            .set_name("D01")
        )

    def _d02(self, *, is_standalone: bool) -> pp.ParserElement:
        return (
            self._command(
                pp.Opt(self._coordinate_x.set_results_name("x"))
                + pp.Opt(self._coordinate_y.set_results_name("y"))
                + pp.Regex(r"D0*2")
            )
            .set_parse_action(
                self.make_unpack_callback(D02, is_standalone=is_standalone)
            )
            .set_name("D02")
        )

    def _d03(self, *, is_standalone: bool) -> pp.ParserElement:
        return (
            self._command(
                pp.Opt(self._coordinate_x.set_results_name("x"))
                + pp.Opt(self._coordinate_y.set_results_name("y"))
                + pp.Regex(r"D0*3")
            )
            .set_parse_action(
                self.make_unpack_callback(D03, is_standalone=is_standalone)
            )
            .set_name("D03")
        )

    #  ██████      █████ ███████ ██████  ███████ ███████
    # ██          ██     ██   ██ ██   ██ ██      ██
    # ██   ███    ██     ██   ██ ██   ██ █████   ███████
    # ██    ██    ██     ██   ██ ██   ██ ██           ██
    #  ██████      █████ ███████ ██████  ███████ ███████

    @pp.cached_property
    def g_codes(self) -> pp.ParserElement:
        """Create a parser element capable of parsing G-codes."""
        g04_comment = self._command(
            pp.Regex(r"G0*4") + pp.Opt(self.string),
        ).set_name("G04")

        if self.optimization & Optimization.DISCARD_COMMENTS:
            g04_comment = pp.Suppress(g04_comment)
        else:
            g04_comment = g04_comment.set_parse_action(self.make_unpack_callback(G04))

        def _standalone(cls: Type[Node]) -> pp.ParserElement:
            code = int(cls.__qualname__.lstrip("G"))
            return (
                self._command(pp.Regex(f"G0*{code}"))
                .set_name(cls.__qualname__)
                .set_parse_action(self.make_unpack_callback(cls, is_standalone=True))
            )

        def _non_standalone(cls: Type[Node]) -> pp.ParserElement:
            # We have to account for legacy cases like `G70D02*`, see
            # `G.is_standalone` docstring for more information.
            code = int(cls.__qualname__.lstrip("G"))
            return (
                (
                    pp.Regex(f"G0*{code}")
                    + pp.FollowedBy(pp.one_of(["D", "X", "Y", "I", "J"]))
                )
                .set_name(cls.__qualname__)
                .set_parse_action(self.make_unpack_callback(cls, is_standalone=False))
            ) + self.d_codes_non_standalone

        if self.syntax_switches.allow_non_standalone_d_codes:
            non_standalone_codes: Iterable[pp.ParserElement] = (
                _non_standalone(cast(Type[Node], cls))
                for cls in reversed(
                    (
                        G01,
                        G02,
                        G03,
                        G36,
                        G37,
                        G54,
                        G55,
                        G70,
                        G71,
                        G74,
                        G75,
                        G90,
                        G91,
                    )
                )
            )
        else:
            non_standalone_codes = ()

        return pp.MatchFirst(
            [
                g04_comment,
                *(
                    _standalone(cast(Type[Node], cls))
                    for cls in reversed(
                        (
                            G01,
                            G02,
                            G03,
                            G36,
                            G37,
                            G54,
                            G55,
                            G70,
                            G71,
                            G74,
                            G75,
                            G90,
                            G91,
                        )
                    )
                ),
                *non_standalone_codes,
            ]
        )

    # ██      ██████   █████  ██████      █████ ███████ ███    ███ ███    ███  █████  ███    ██ ██████  ███████ # noqa: E501
    # ██     ██    ██ ██   ██ ██   ██    ██     ██   ██ ████  ████ ████  ████ ██   ██ ████   ██ ██   ██ ██      # noqa: E501
    # ██     ██    ██ ███████ ██   ██    ██     ██   ██ ██ ████ ██ ██ ████ ██ ███████ ██ ██  ██ ██   ██ ███████ # noqa: E501
    # ██     ██    ██ ██   ██ ██   ██    ██     ██   ██ ██  ██  ██ ██  ██  ██ ██   ██ ██  ██ ██ ██   ██      ██ # noqa: E501
    # ██████ ███████  ██   ██ ██████      █████ ███████ ██      ██ ██      ██ ██   ██ ██   ████ ██████  ███████ # noqa: E501

    @pp.cached_property
    def load_commands(self) -> pp.ParserElement:
        """Create a parser element capable of parsing Load-commands."""
        return pp.MatchFirst([self.ln(), self.lp(), self.lr(), self.ls(), self.lm()])

    def ln(self) -> pp.ParserElement:
        """Create a parser for the LN command."""
        return (
            self._extended_command(
                pp.Literal("LN") + self.string.set_results_name("name")
            )
            .set_parse_action(self.make_unpack_callback(LN))
            .set_name("LN")
        )

    def lp(self) -> pp.ParserElement:
        """Create a parser for the LP command."""
        return (
            self._extended_command(
                pp.Literal("LP") + pp.one_of(["C", "D"]).set_results_name("polarity")
            )
            .set_parse_action(self.make_unpack_callback(LP))
            .set_name("LP")
        )

    def lr(self) -> pp.ParserElement:
        """Create a parser for the LR command."""
        return (
            self._extended_command(
                pp.Literal("LR") + self.double.set_results_name("rotation")
            )
            .set_parse_action(self.make_unpack_callback(LR))
            .set_name("LR")
        )

    def ls(self) -> pp.ParserElement:
        """Create a parser for the LS command."""
        return (
            self._extended_command(
                pp.Literal("LS") + self.double.set_results_name("scale")
            )
            .set_parse_action(self.make_unpack_callback(LS))
            .set_name("LS")
        )

    def lm(self) -> pp.ParserElement:
        """Create a parser for the LM command."""
        return (
            self._extended_command(
                pp.Literal("LM")
                + pp.one_of(["N", "XY", "X", "Y"]).set_results_name("mirroring")
            )
            .set_parse_action(self.make_unpack_callback(LM))
            .set_name("LM")
        )

    # ███    ███     █████ ███████ ██████  ███████ ███████
    # ████  ████    ██     ██   ██ ██   ██ ██      ██
    # ██ ████ ██    ██     ██   ██ ██   ██ █████   ███████
    # ██  ██  ██    ██     ██   ██ ██   ██ ██           ██
    # ██      ██     █████ ███████ ██████  ███████ ███████

    @pp.cached_property
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

    def _cb(self, element: pp.ParserElement, cls: Type[Node]) -> pp.ParserElement:
        return element.set_parse_action(self.make_unpack_callback(cls))

    @pp.cached_property
    def expression(self) -> pp.ParserElement:
        """Create a parser element capable of parsing expressions."""
        expr = pp.Forward()
        factor = (
            self.variable
            | self.constant
            | self._cb(pp.Literal("(") + expr("inner") + pp.Literal(")"), Parenthesis)
        )("factor")

        last_expr = factor
        # Unary - operator
        op_expr = pp.Literal("-")

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(op_expr + this_expr) + (
            op_expr + this_expr("operand")
        ).set_parse_action(self.make_unpack_callback(Neg))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        # Unary + operator
        op_expr = pp.Literal("+")

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(op_expr + this_expr) + (
            op_expr + this_expr("operand")
        ).set_parse_action(self.make_unpack_callback(Pos))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        # Binary / operator
        op_expr = pp.Literal("/")

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(last_expr + op_expr + last_expr) + (
            last_expr("head")
            + (op_expr + last_expr.set_results_name("tail", list_all_matches=True))[
                1, ...
            ]
        ).set_parse_action(self.make_unpack_callback(Div))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        # Binary x|X operator
        op_expr = pp.one_of(["x", "X"])

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(last_expr + op_expr + last_expr) + (
            last_expr("head")
            + (op_expr + last_expr.set_results_name("tail", list_all_matches=True))[
                1, ...
            ]
        ).set_parse_action(self.make_unpack_callback(Mul))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        # Binary - operator
        op_expr = pp.Literal("-")

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(last_expr + op_expr + last_expr) + (
            last_expr("head")
            + (op_expr + last_expr.set_results_name("tail", list_all_matches=True))[
                1, ...
            ]
        ).set_parse_action(self.make_unpack_callback(Sub))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        # Binary - operator
        op_expr = pp.Literal("+")

        this_expr = pp.Forward()
        match_expr = pp.FollowedBy(last_expr + op_expr + last_expr) + (
            last_expr("head")
            + (op_expr + last_expr.set_results_name("tail", list_all_matches=True))[
                1, ...
            ]
        ).set_parse_action(self.make_unpack_callback(Add))
        this_expr <<= match_expr | last_expr
        last_expr = this_expr

        expr <<= last_expr

        return take_only(expr("expression"), "expression")

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
            self._command(self.variable + "=" + self.expression)
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

    @pp.cached_property
    def properties(self) -> pp.ParserElement:
        """Create a parser element capable of parsing Properties-commands."""
        return pp.MatchFirst(
            [
                self.fs(),
                self.mo(),
                self.ip(),
                self.ir(),
                self.of(),
                self.as_(),
                self.mi(),
                self.in_(),
                self.sf(),
            ]
        )

    def fs(self) -> pp.ParserElement:
        """Create a parser for the FS command."""
        return (
            self._extended_command(
                pp.Literal("FS")
                + pp.one_of(("L", "T", "")).set_results_name("zeros")
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

    def of(self) -> pp.ParserElement:
        """Create a parser for the MO command."""
        return (
            self._extended_command(
                pp.Literal("OF")
                + pp.Opt(pp.Literal("A") + self.double.set_results_name("a_offset"))
                + pp.Opt(pp.Literal("B") + self.double.set_results_name("b_offset"))
            )
            .set_parse_action(self.make_unpack_callback(OF))
            .set_name("OF")
        )

    def as_(self) -> pp.ParserElement:
        """Create a parser element capable of parsing AS-commands."""
        return (
            self._extended_command(
                pp.Literal("AS")
                + pp.one_of(["AXBY", "AYBX"]).set_results_name("correspondence")
            )
            .set_parse_action(self.make_unpack_callback(AS))
            .set_name("OF")
        )

    def mi(self) -> pp.ParserElement:
        """Create a parser for the MI command."""
        return (
            self._extended_command(
                pp.Literal("MI")
                + pp.Opt(pp.Literal("A") + self.boolean.set_results_name("a_mirroring"))
                + pp.Opt(pp.Literal("B") + self.boolean.set_results_name("b_mirroring"))
            )
            .set_parse_action(self.make_unpack_callback(MI))
            .set_name("MI")
        )

    def in_(self) -> pp.ParserElement:
        """Create a parser for the IN command."""
        return (
            self._extended_command(
                pp.Literal("IN") + self.string.set_results_name("name")
            )
            .set_parse_action(self.make_unpack_callback(IN))
            .set_name("IN")
        )

    def sf(self) -> pp.ParserElement:
        """Create a parser for the SF command."""
        return (
            self._extended_command(
                pp.Literal("SF")
                + pp.Opt(pp.Literal("A") + self.double.set_results_name("a_scale"))
                + pp.Opt(pp.Literal("B") + self.double.set_results_name("b_scale"))
            )
            .set_parse_action(self.make_unpack_callback(SF))
            .set_name("SF")
        )

    @pp.cached_property
    def _invalid_token(self) -> pp.ParserElement:
        syntax = pp.Combine(pp.Regex(r".+"))
        return (
            syntax.set_results_name("string")
            .set_name("Invalid")
            .set_parse_action(self.make_unpack_callback(Invalid))
        )


def take_only(expr: pp.ParserElement, name: str) -> pp.ParserElement:
    """Add parse action to extract single named parse result from a parse result."""
    return pp.TokenConverter(expr).add_parse_action(lambda t: t.as_dict()[name])(name)
