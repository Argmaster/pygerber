"""GerberX3 grammar."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, TypeVar

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
    ungroup,
)

from pygerber.gerberx3.tokenizer.tokens.ab_block_aperture import (
    BlockApertureBegin,
    BlockApertureEnd,
)
from pygerber.gerberx3.tokenizer.tokens.ad_define_aperture import (
    DefineCircle,
    DefineMacro,
    DefineObround,
    DefinePolygon,
    DefineRectangle,
)
from pygerber.gerberx3.tokenizer.tokens.as_axis_select import AxisSelect
from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
from pygerber.gerberx3.tokenizer.tokens.d01_draw import D01Draw
from pygerber.gerberx3.tokenizer.tokens.d02_move import D02Move
from pygerber.gerberx3.tokenizer.tokens.d03_flash import D03Flash
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture
from pygerber.gerberx3.tokenizer.tokens.end_of_expression import EndOfExpression
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import CoordinateFormat
from pygerber.gerberx3.tokenizer.tokens.g01_set_linear import SetLinear
from pygerber.gerberx3.tokenizer.tokens.g02_set_clockwise_circular import (
    SetClockwiseCircular,
)
from pygerber.gerberx3.tokenizer.tokens.g03_set_counterclockwise_circular import (
    SetCounterclockwiseCircular,
)
from pygerber.gerberx3.tokenizer.tokens.g04_comment import Comment
from pygerber.gerberx3.tokenizer.tokens.g36_begin_region import BeginRegion
from pygerber.gerberx3.tokenizer.tokens.g37_end_region import EndRegion
from pygerber.gerberx3.tokenizer.tokens.g54_select_aperture import G54SelectAperture
from pygerber.gerberx3.tokenizer.tokens.g70_set_unit_inch import SetUnitInch
from pygerber.gerberx3.tokenizer.tokens.g71_set_unit_mm import SetUnitMillimeters
from pygerber.gerberx3.tokenizer.tokens.g75_multi_quadrant import SetMultiQuadrantMode
from pygerber.gerberx3.tokenizer.tokens.g90_set_coordinate_absolute import (
    SetAbsoluteNotation,
)
from pygerber.gerberx3.tokenizer.tokens.g91_set_coordinate_incremental import (
    SetIncrementalNotation,
)
from pygerber.gerberx3.tokenizer.tokens.groups.ast import AST
from pygerber.gerberx3.tokenizer.tokens.groups.statement import (
    Statement,
)
from pygerber.gerberx3.tokenizer.tokens.in_image_name import ImageName
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
    AdditionOperator,
    DivisionOperator,
    MultiplicationOperator,
    NegationOperator,
    PositiveOperator,
    SubtractionOperator,
)
from pygerber.gerberx3.tokenizer.tokens.macro.comment import MacroComment
from pygerber.gerberx3.tokenizer.tokens.macro.macro_begin import MacroBegin
from pygerber.gerberx3.tokenizer.tokens.macro.numeric_constant import NumericConstant
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
from pygerber.gerberx3.tokenizer.tokens.of_image_offset import ImageOffset
from pygerber.gerberx3.tokenizer.tokens.sr_step_repeat import (
    StepRepeatBegin,
    StepRepeatEnd,
)
from pygerber.gerberx3.tokenizer.tokens.ta_aperture_attribute import ApertureAttribute
from pygerber.gerberx3.tokenizer.tokens.td_delete_attribute import DeleteAttribute
from pygerber.gerberx3.tokenizer.tokens.tf_file_attribute import FileAttribute
from pygerber.gerberx3.tokenizer.tokens.to_object_attribute import ObjectAttribute

if TYPE_CHECKING:
    from typing_extensions import Self


T1 = TypeVar("T1")
T2 = TypeVar("T2")


class TokenWrapper:
    """Class for wrapping ParserElements with Token classes."""

    def __init__(self, *, is_raw: bool) -> None:
        self.is_raw = is_raw

    def __call__(
        self,
        token_cls: type[Token],
        parser_element: ParserElement,
    ) -> ParserElement:
        """Wrap ParserElement with Token class."""
        if self.is_raw:
            return parser_element

        return token_cls.wrap(parser_element)

    @classmethod
    def build(
        cls,
        wrapper: Optional[Self] = None,
        *,
        is_raw: bool = False,
    ) -> Self:
        """Build TokenWrapper instance."""
        if wrapper is not None:
            return wrapper

        return cls(is_raw=is_raw)


class GrammarBuilder:
    """Base class for all grammar builder classes."""

    def __init__(
        self,
        wrapper: Optional[TokenWrapper] = None,
        *,
        is_raw: bool = False,
    ) -> None:
        self.wrapper = TokenWrapper.build(wrapper=wrapper, is_raw=is_raw)


class GerberGrammarBuilder(GrammarBuilder):
    """Base class for all Gerber grammar builders."""

    def build(self) -> GerberGrammar:
        """Build grammar object."""
        wrapper = self.wrapper
        eoex = self._build_eoex()

        load_commands = self._build_load_commands()
        # Sets the polarity of the whole image.
        ip = self._build_stmt(
            wrapper(
                ImagePolarity,
                Literal("IP") + oneOf("POS NEG").set_results_name("image_polarity"),
            ),
        )
        # End of file.
        m02 = wrapper(
            M02EndOfFile,
            Literal("M02").set_name("End of file") + eoex,
        )
        # Optional stop.
        m01 = wrapper(M01OptionalStop, Literal("M01").set_name("Optional stop") + eoex)
        # Program stop.
        m00 = wrapper(M00ProgramStop, Literal("M00").set_name("Program stop") + eoex)

        dnn = wrapper(DNNSelectAperture, self._build_aperture_identifier() + eoex)
        """Sets the current aperture to D code nn."""

        fs = self._build_format_specifier()
        # Sets the unit to mm or inch.
        mo = self._build_stmt(
            wrapper(
                UnitMode,
                Literal("MO")
                + oneOf("MM IN").set_results_name("unit").set_name("unit"),
            ),
        )

        # Open a step and repeat statement.
        sr = self._build_step_repeat()

        # Opens a block aperture statement and assigns its aperture number
        ab_open = self._build_stmt(
            wrapper(
                BlockApertureBegin,
                Literal("AB") + self._build_aperture_identifier(),
            ),
        )
        # Closes a block aperture statement.
        ab_close = self._build_stmt(wrapper(BlockApertureEnd, Literal("AB")))

        g_codes = self._build_g_codes()
        d_codes = self._build_d_codes()

        common = (
            self._build_comment_token()
            | mo
            | fs
            | self._build_macro_tokens()
            | self._build_define_aperture()
            | dnn
            | (d_codes + eoex)
            | (g_codes + d_codes + eoex)
            | (g_codes + eoex)
            | load_commands
            | ip
            | ab_open
            | ab_close
            | sr
            | self._build_attribute_tokens(statement=True)
            | eoex
        )

        expressions = self.wrapper(AST, (common | m02 | m01 | m00)[0, ...])
        grammar = self.wrapper(AST, common[0, ...] + (m02 | m01 | m00))

        return GerberGrammar(grammar, expressions)

    def _build_load_commands(self) -> ParserElement:
        wrapper = self.wrapper

        lm = self._build_stmt(
            wrapper(
                LoadMirroring,
                Literal("LM") + oneOf("N XY Y X").set_results_name("mirroring"),
            ),
        )
        lp = self._build_stmt(
            wrapper(
                LoadPolarity,
                Literal("LP") + oneOf("C D").set_results_name("polarity"),
            ),
        )
        ls = self._build_stmt(
            wrapper(LoadScaling, Literal("LS") + self._build_decimal("scaling")),
        )
        lr = self._build_stmt(
            wrapper(LoadRotation, Literal("LR") + self._build_decimal("rotation")),
        )
        ln = self._build_stmt(
            wrapper(LoadName, Literal("LN") + self._build_string()),
        )
        in_ = self._build_stmt(
            wrapper(ImageName, Literal("IN") + self._build_string()),
        )
        as_ = self._build_stmt(
            wrapper(
                AxisSelect,
                Literal("AS") + oneOf("AXBY AYBX").set_results_name("correspondence"),
            ),
        )
        of = self._build_stmt(
            wrapper(
                ImageOffset,
                Literal("OF")
                + Opt(Literal("A") + self._build_decimal("a"))
                + Opt(Literal("B") + self._build_decimal("b")),
            ),
        )

        return lm | lp | ls | lr | as_ | of | in_ | ln

    def _build_format_specifier(self) -> ParserElement:
        wrapper = self.wrapper

        coord_digits = Regex(r"[1-9][1-9]")

        # Sets the coordinate format, e.g. the number of decimals.
        return self._build_stmt(
            wrapper(
                CoordinateFormat,
                Literal("FS")
                + oneOf("L T").set_results_name("zeros_mode").set_name("zeros mode")
                + oneOf("A I")
                .set_results_name("coordinate_mode")
                .set_name("coordinate mode")
                + "X"
                + coord_digits.set_results_name("x_format").set_name(
                    "X coordinate format",
                )
                + "Y"
                + coord_digits.set_results_name("y_format").set_name(
                    "Y coordinate format",
                ),
            ),
        )

    def _build_step_repeat(self) -> ParserElement:
        wrapper = self.wrapper

        sr_open = self._build_stmt(
            wrapper(
                StepRepeatBegin,
                Literal("SR")
                + "X"
                + self._build_integer("x_repeat")
                + "Y"
                + self._build_integer("y_repeat")
                + "I"
                + self._build_decimal("x_step")
                + "J"
                + self._build_decimal("y_step"),
            ),
        )
        # Closes a step and repeat statement.
        sr_close = self._build_stmt(wrapper(StepRepeatEnd, Literal("SR")))

        return sr_open | sr_close

    def _build_g_codes(self) -> ParserElement:
        wrapper = self.wrapper

        g54dnn = wrapper(
            G54SelectAperture,
            Literal("G54") + self._build_aperture_identifier(),
        )
        g01 = wrapper(SetLinear, Regex("G0*1"))
        g02 = wrapper(SetClockwiseCircular, Regex("G0*2"))
        g03 = wrapper(SetCounterclockwiseCircular, Regex("G0*3"))
        g36 = wrapper(BeginRegion, Regex("G0*36"))
        g37 = wrapper(EndRegion, Regex("G0*37"))
        g70 = wrapper(SetUnitInch, Regex("G0*70"))
        g71 = wrapper(SetUnitMillimeters, Regex("G0*71"))
        g74 = wrapper(SetMultiQuadrantMode, Regex("G0*74"))
        g75 = wrapper(SetMultiQuadrantMode, Regex("G0*75"))
        g90 = wrapper(SetAbsoluteNotation, Regex("G0*90"))
        g91 = wrapper(SetIncrementalNotation, Regex("G0*91"))

        # Order is important, as g03 would match g36 if checked before g36 regex.
        return g54dnn | g36 | g37 | g70 | g71 | g74 | g75 | g90 | g91 | g01 | g02 | g03

    def _build_d_codes(self) -> ParserElement:
        wrapper = self.wrapper

        x_coordinate = Literal("X") + self._build_integer("x", "X coordinate")
        y_coordinate = Literal("Y") + self._build_integer("y", "Y coordinate")

        i_coordinate = Literal("I") + self._build_integer("i", "I offset")
        j_coordinate = Literal("J") + self._build_integer("j", "J offset")

        xy = (x_coordinate + Opt(y_coordinate)) | (Opt(x_coordinate) + y_coordinate)
        ij = (i_coordinate + Opt(j_coordinate)) | (Opt(i_coordinate) + j_coordinate)

        d01 = wrapper(
            D01Draw,
            ((Opt(xy) + Opt(ij) + Regex("D0*1")) | (xy + Opt(ij))),
        )
        d02 = wrapper(
            D02Move,
            Opt(xy) + Regex("D0*2"),
        )
        d03 = wrapper(
            D03Flash,
            Opt(xy) + Regex("D0*3"),
        )

        return d03 | d02 | d01

    def _build_comment_token(self) -> ParserElement:
        wrapper = self.wrapper
        eoex = self._build_eoex()

        # A human readable comment, does not affect the image.
        return wrapper(Comment, Literal("G04") + self._build_string() + eoex)

    def _build_define_aperture(self) -> ParserElement:
        wrapper = self.wrapper

        ad = Literal("AD").set_name("AD code")

        circle = wrapper(
            DefineCircle,
            ad
            + self._build_aperture_identifier()
            + Literal("C").set_results_name("aperture_type")
            + ","
            + self._build_decimal("diameter")
            + Opt("X" + self._build_decimal("hole_diameter")),
        ).set_name("define aperture circle")

        rectangle = wrapper(
            DefineRectangle,
            ad
            + self._build_aperture_identifier()
            + Literal("R").set_results_name("aperture_type")
            + ","
            + self._build_decimal("x_size")
            + "X"
            + self._build_decimal("y_size")
            + Opt("X" + self._build_decimal("hole_diameter")),
        ).set_name("define aperture rectangle")

        obround = wrapper(
            DefineObround,
            ad
            + self._build_aperture_identifier()
            + Literal("O").set_results_name("aperture_type")
            + ","
            + self._build_decimal("x_size")
            + "X"
            + self._build_decimal("y_size")
            + Opt("X" + self._build_decimal("hole_diameter")),
        ).set_name("define aperture obround")

        polygon = wrapper(
            DefinePolygon,
            ad
            + self._build_aperture_identifier()
            + Literal("P").set_results_name("aperture_type")
            + ","
            + self._build_decimal("outer_diameter")
            + "X"
            + self._build_decimal("number_of_vertices")
            + Opt(
                "X"
                + self._build_decimal("rotation")
                + Opt("X" + self._build_decimal("hole_diameter")),
            ),
        ).set_name("define aperture polygon")

        am_param = self._build_decimal("am_param", list_all_matches=True)
        # Defines a template-based aperture, assigns a D code to it.

        macro = wrapper(
            DefineMacro,
            ad
            + self._build_aperture_identifier()
            + self._build_name("aperture_type")
            + Opt("," + am_param + ZeroOrMore("X" + am_param)),
        ).set_name("define aperture macro")

        return self._build_stmt(circle | rectangle | obround | polygon | macro)

    def _build_macro_tokens(self) -> ParserElement:
        wrapper = self.wrapper

        primitive = self._build_macro_primitive()
        variable_definition = self._build_macro_variable_definition()
        comment = self._build_comment_token()

        macro_body = (
            (primitive | variable_definition | comment)
            .set_results_name("macro_body", list_all_matches=True)
            .set_name("macro body expression")
        )[1, ...]

        am_start = (
            self._annotate_parser_element(
                wrapper(
                    MacroBegin,
                    Literal("AM") + self._build_name("macro_name"),
                ),
                "macro_begin",
            )
            + self._build_eoex()
        )

        # Defines a macro aperture template.
        return self._build_stmt(
            wrapper(
                MacroDefinition,
                am_start + macro_body,
            ),
            eoex=False,
        ).set_name("macro definition")

    def _build_macro_variable_definition(self) -> ParserElement:
        return self.wrapper(
            MacroVariableDefinition,
            self._build_macro_variable()
            + "="
            + self._build_macro_expr("value")
            + self._build_eoex(),
        )

    def _build_macro_primitive(self) -> ParserElement:
        cs = Suppress(Literal(",").set_name("comma"))
        primitive_comment = self.wrapper(MacroComment, "0" + self._build_string())
        primitive_circle = self.wrapper(
            PrimitiveCircle,
            "1"  # Circle
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("diameter")  # Diameter
            + cs
            + self._build_macro_expr("center_x")  # Center X
            + cs
            + self._build_macro_expr("center_y")  # Center Y
            + Opt(cs + self._build_macro_expr("rotation")),  # Rotation
        )
        primitive_vector_line = self.wrapper(
            PrimitiveVectorLine,
            "20"  # Vector Line
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("width")  # Width
            + cs
            + self._build_macro_expr("start_x")  # Start X
            + cs
            + self._build_macro_expr("start_y")  # Start Y
            + cs
            + self._build_macro_expr("end_x")  # End X
            + cs
            + self._build_macro_expr("end_y")  # End Y
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )
        primitive_center_line = self.wrapper(
            PrimitiveCenterLine,
            "21"  # Center Line
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("width")  # Width
            + cs
            + self._build_macro_expr("hight")  # Hight
            + cs
            + self._build_macro_expr("center_x")  # Center X
            + cs
            + self._build_macro_expr("center_y")  # Center Y
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )
        primitive_outline = self.wrapper(
            PrimitiveOutline,
            "4"  # Outline
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("number_of_vertices")  # Number of vertices
            + cs
            + self._build_macro_expr("start_x")  # Start X
            + cs
            + self._build_macro_expr("start_y")  # Start Y
            + OneOrMore(  # Subsequent points...
                self._build_macro_point().set_results_name(
                    "point",
                    list_all_matches=True,
                ),
            )
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )
        primitive_polygon = self.wrapper(
            PrimitivePolygon,
            "5"  # Polygon
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("number_of_vertices")  # Number of vertices
            + cs
            + self._build_macro_expr("center_x")  # Center X
            + cs
            + self._build_macro_expr("center_y")  # Center Y
            + cs
            + self._build_macro_expr("diameter")  # Diameter
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )
        primitive_thermal = self.wrapper(
            PrimitiveThermal,
            "7"  # Thermal
            + cs
            + self._build_macro_expr("center_x")  # Center X
            + cs
            + self._build_macro_expr("center_y")  # Center Y
            + cs
            + self._build_macro_expr("outer_diameter")  # Outer diameter
            + cs
            + self._build_macro_expr("inner_diameter")  # Inner diameter
            + cs
            + self._build_macro_expr("gap")  # Gap
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )

        return (
            (primitive_comment + self._build_eoex()).set_name("primitive comment")
            | (primitive_circle + self._build_eoex()).set_name("primitive circle")
            | (primitive_vector_line + self._build_eoex()).set_name(
                "primitive vector line",
            )
            | (primitive_center_line + self._build_eoex()).set_name(
                "primitive center line",
            )
            | (primitive_outline + self._build_eoex()).set_name("primitive outline")
            | (primitive_polygon + self._build_eoex()).set_name("primitive polygon")
            | (primitive_thermal + self._build_eoex()).set_name("primitive thermal")
        )

    def _build_macro_point(self) -> ParserElement:
        cs = Suppress(Literal(",").set_name("comma"))
        return self.wrapper(
            Point,
            cs + self._build_macro_expr("x") + cs + self._build_macro_expr("y"),
        )

    _macro_expr: Optional[ParserElement] = None

    def _build_macro_expr(self, expr_name: str = "expr") -> ParserElement:
        macro_variable = self._build_macro_variable()
        numeric_constant = self.wrapper(
            NumericConstant,
            Regex(r"((([0-9]+)(\.[0-9]*)?)|(\.[0-9]+))").set_results_name(
                "numeric_constant_value",
            ),
        )

        arithmetic_expression = Forward()

        factor = macro_variable | numeric_constant

        if self.wrapper.is_raw:
            arithmetic_expression <<= ungroup(
                infix_notation(
                    factor,
                    [
                        ("-", 1, OpAssoc.RIGHT),
                        ("+", 1, OpAssoc.RIGHT),
                        ("/", 2, OpAssoc.RIGHT),
                        (oneOf("x X"), 2, OpAssoc.RIGHT),
                        ("-", 2, OpAssoc.RIGHT),
                        ("+", 2, OpAssoc.RIGHT),
                    ],
                ),
            )
        else:
            arithmetic_expression <<= ungroup(
                infix_notation(
                    factor,
                    [
                        (
                            Suppress("-"),
                            1,
                            OpAssoc.RIGHT,
                            NegationOperator.new,
                        ),
                        (
                            Suppress("+"),
                            1,
                            OpAssoc.RIGHT,
                            PositiveOperator.new,
                        ),
                        (
                            Suppress("/"),
                            2,
                            OpAssoc.RIGHT,
                            DivisionOperator.new,
                        ),
                        (
                            Suppress(oneOf("x X")),
                            2,
                            OpAssoc.RIGHT,
                            MultiplicationOperator.new,
                        ),
                        (
                            Suppress("-"),
                            2,
                            OpAssoc.RIGHT,
                            SubtractionOperator.new,
                        ),
                        (
                            Suppress("+"),
                            2,
                            OpAssoc.RIGHT,
                            AdditionOperator.new,
                        ),
                    ],
                ),
            )

        expr = arithmetic_expression | factor

        return expr.set_results_name(expr_name).set_name(expr_name)

    def _build_macro_variable(self) -> ParserElement:
        return self.wrapper(
            MacroVariableName,
            Regex(r"\$[0-9]*[1-9][0-9]*")("macro_variable_name"),
        )

    def _build_attribute_tokens(self, *, statement: bool = False) -> ParserElement:
        wrapper = self.wrapper

        file_attribute_name = (
            oneOf(
                ".Part .FileFunction .FilePolarity .SameCoordinates .CreationDate\
                .GenerationSoftware .ProjectId .MD5",
            )
            | self._build_user_name()
        ).set_name("file attribute name")

        aperture_attribute_name = (
            oneOf(".AperFunction .DrillTolerance .FlashText") | self._build_user_name()
        ).set_name("aperture attribute name")

        object_attribute_name = (
            oneOf(
                ".N .P .C .CRot .CMfr .CMPN .CVal .CMnt .CFtp .CPgN .CPgD .CHgt .CLbN "
                ".CLbD .CSup",
            )
            | self._build_user_name()
        ).set_name("object attribute name")

        # Set a file attribute.
        tf = wrapper(
            FileAttribute,
            Literal("TF")
            + file_attribute_name.set_results_name("attribute_name")
            + ZeroOrMore("," + (self._build_field(list_all_matches=True) | "")),
        )
        # Add an aperture attribute to the dictionary or modify it.
        ta = wrapper(
            ApertureAttribute,
            Literal("TA")
            + aperture_attribute_name.set_results_name("attribute_name")
            + ZeroOrMore("," + (self._build_field(list_all_matches=True) | "")),
        )
        # Add an object attribute to the dictionary or modify it.
        to = wrapper(
            ObjectAttribute,
            Literal("TO")
            + object_attribute_name.set_results_name("attribute_name")
            + ZeroOrMore("," + (self._build_field(list_all_matches=True) | "")),
        )
        # Delete one or all attributes in the dictionary.
        td = wrapper(
            DeleteAttribute,
            Literal("TD")
            + Opt(
                file_attribute_name
                | aperture_attribute_name
                | object_attribute_name
                | self._build_user_name(),
            ).set_results_name("attribute_name"),
        )
        if statement:
            return self._build_stmt(tf | ta | to | td)

        return tf | ta | to | td

    def _build_eoex(self) -> ParserElement:
        return self.wrapper(EndOfExpression, Literal("*").set_name("end of expression"))

    def _build_stmt(
        self,
        expr: ParserElement,
        *,
        eoex: bool = True,
    ) -> ParserElement:
        begin_stmt = Literal("%")
        end_stmt = Literal("%")

        return self.wrapper(
            Statement,
            begin_stmt + expr + ((self._build_eoex() + end_stmt) if eoex else end_stmt),
        )

    def _build_integer(
        self,
        result_name: str = "integer",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            Combine(Opt(oneOf("+ -")) + Word(nums)),
            result_name,
            name,
            **kwargs,
        )

    def _annotate_parser_element(
        self,
        element: ParserElement,
        result_name: str,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        if name is None:
            name = result_name
        return element.set_name(name).set_results_name(result_name, **kwargs)

    def _build_decimal(
        self,
        result_name: str = "decimal",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            Regex(r"[+-]?((([0-9]+)(\.[0-9]*)?)|(\.[0-9]+))"),
            result_name,
            name,
            **kwargs,
        )

    def _build_aperture_identifier(
        self,
        result_name: str = "aperture_identifier",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            Combine("D" + Regex(r"[1-9][0-9]+")),
            result_name,
            name,
            **kwargs,
        )

    def _build_name(
        self,
        result_name: str = "name",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            Regex(r"[._a-zA-Z$][\._a-zA-Z0-9]*"),
            result_name,
            name,
            **kwargs,
        )

    def _build_user_name(
        self,
        result_name: str = "user_name",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            Regex(r"[_a-zA-Z$][\._a-zA-Z0-9]*"),
            result_name,
            name,
            **kwargs,
        )

    def _build_string(
        self,
        result_name: str = "string",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            CharsNotIn("%*"),
            result_name,
            name,
            **kwargs,
        )

    def _build_field(
        self,
        result_name: str = "field",
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> ParserElement:
        return self._annotate_parser_element(
            CharsNotIn("%*"),
            result_name,
            name,
            **kwargs,
        )


class GerberGrammar:
    """Gerber grammar container."""

    def __init__(
        self,
        strict_grammar: ParserElement,
        expression_grammar: ParserElement,
    ) -> None:
        self.strict_grammar = strict_grammar
        self.expression_grammar = expression_grammar
