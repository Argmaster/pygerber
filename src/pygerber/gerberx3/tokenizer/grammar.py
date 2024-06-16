"""GerberX3 grammar."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

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
from pygerber.gerberx3.tokenizer.tokens.g74_single_quadrant import SetSingleQuadrantMode
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
from pygerber.gerberx3.tokenizer.tokens.invalid_token import InvalidToken
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
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.binary import (
    AdditionOperator,
    DivisionOperator,
    MultiplicationOperator,
    SubtractionOperator,
)
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.numeric_constant import (
    NumericConstant,
)
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.unary import (
    NegationOperator,
    PositiveOperator,
)
from pygerber.gerberx3.tokenizer.tokens.macro.expressions.variable_name import (
    MacroVariableName,
)
from pygerber.gerberx3.tokenizer.tokens.macro.macro_begin import MacroBegin
from pygerber.gerberx3.tokenizer.tokens.macro.point import Point
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_1_circle import (
    Code1CircleToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_4_outline import (
    Code4OutlineToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_5_polygon import (
    Code5PolygonToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_7_thermal import (
    Code7ThermalToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_20_vector_line import (
    Code20VectorLineToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_21_center_line import (
    Code21CenterLineToken,
)
from pygerber.gerberx3.tokenizer.tokens.macro.statements.comment import MacroComment
from pygerber.gerberx3.tokenizer.tokens.macro.statements.variable_assignment import (
    MacroVariableAssignment,
)
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
        token_cls: Type[Token],
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


class GrammarBuilderOptions:
    """Grammar builder options."""


@dataclass
class GrammarBuilder:
    """Base class for all grammar builder classes."""

    def __init__(
        self,
        wrapper: Optional[TokenWrapper] = None,
        *,
        is_raw: bool = False,
        options: Optional[GrammarBuilderOptions] = None,
    ) -> None:
        self.wrapper = TokenWrapper.build(wrapper=wrapper, is_raw=is_raw)
        self.options = options if options is not None else GrammarBuilderOptions()


@dataclass
class GerberGrammarBuilderOptions(GrammarBuilderOptions):
    """Grammar builder options."""

    ast_token_cls: Type[Token] = AST
    block_aperture_begin_token_cls: Type[Token] = BlockApertureBegin
    block_aperture_end_token_cls: Type[Token] = BlockApertureEnd
    define_circle_token_cls: Type[Token] = DefineCircle
    define_macro_token_cls: Type[Token] = DefineMacro
    define_obround_token_cls: Type[Token] = DefineObround
    define_polygon_token_cls: Type[Token] = DefinePolygon
    define_rectangle_token_cls: Type[Token] = DefineRectangle
    axis_select_token_cls: Type[Token] = AxisSelect
    d01_draw_token_cls: Type[Token] = D01Draw
    d02_move_token_cls: Type[Token] = D02Move
    d03_flash_token_cls: Type[Token] = D03Flash
    dnn_select_aperture_token_cls: Type[Token] = DNNSelectAperture
    end_of_expression_token_cls: Type[Token] = EndOfExpression
    fs_coordinate_format_token_cls: Type[Token] = CoordinateFormat
    g01_set_linear_token_cls: Type[Token] = SetLinear
    g02_set_clockwise_circular_token_cls: Type[Token] = SetClockwiseCircular
    g03_set_counterclockwise_circular_token_cls: Type[Token] = (
        SetCounterclockwiseCircular
    )
    g04_comment_token_cls: Type[Token] = Comment
    g36_begin_region_token_cls: Type[Token] = BeginRegion
    g37_end_region_token_cls: Type[Token] = EndRegion
    g54_select_aperture_token_cls: Type[Token] = G54SelectAperture
    g70_set_unit_inch_token_cls: Type[Token] = SetUnitInch
    g71_set_unit_mm_token_cls: Type[Token] = SetUnitMillimeters
    g74_single_quadrant_token_cls: Type[Token] = SetSingleQuadrantMode
    g75_multi_quadrant_token_cls: Type[Token] = SetMultiQuadrantMode
    g90_set_coordinate_absolute_token_cls: Type[Token] = SetAbsoluteNotation
    g91_set_coordinate_incremental_token_cls: Type[Token] = SetIncrementalNotation
    statement_token_cls: Type[Token] = Statement
    in_image_name_token_cls: Type[Token] = ImageName
    invalid_token_cls: Type[Token] = InvalidToken
    ip_image_polarity_token_cls: Type[Token] = ImagePolarity
    lm_load_mirroring_token_cls: Type[Token] = LoadMirroring
    ln_load_name_token_cls: Type[Token] = LoadName
    lp_load_polarity_token_cls: Type[Token] = LoadPolarity
    lr_load_rotation_token_cls: Type[Token] = LoadRotation
    ls_load_scaling_token_cls: Type[Token] = LoadScaling
    of_image_offset_token_cls: Type[Token] = ImageOffset
    as_axes_select_token_cls: Type[Token] = AxisSelect
    m00_program_stop_token_cls: Type[Token] = M00ProgramStop
    m01_optional_stop_token_cls: Type[Token] = M01OptionalStop
    m02_end_of_file_token_cls: Type[Token] = M02EndOfFile
    macro_definition_token_cls: Type[Token] = MacroDefinition
    macro_addition_operator_token_cls: Type[Token] = AdditionOperator
    macro_division_operator_token_cls: Type[Token] = DivisionOperator
    macro_multiplication_operator_token_cls: Type[Token] = MultiplicationOperator
    macro_negation_operator_token_cls: Type[Token] = NegationOperator
    macro_positive_operator_token_cls: Type[Token] = PositiveOperator
    macro_subtraction_operator_token_cls: Type[Token] = SubtractionOperator
    macro_comment_token_cls: Type[Token] = MacroComment
    macro_begin_token_cls: Type[Token] = MacroBegin
    macro_numeric_constant_token_cls: Type[Token] = NumericConstant
    macro_point_token_cls: Type[Token] = Point
    macro_primitive_center_line_token_cls: Type[Token] = Code21CenterLineToken
    macro_primitive_circle_token_cls: Type[Token] = Code1CircleToken
    macro_primitive_outline_token_cls: Type[Token] = Code4OutlineToken
    macro_primitive_polygon_token_cls: Type[Token] = Code5PolygonToken
    macro_primitive_thermal_token_cls: Type[Token] = Code7ThermalToken
    macro_primitive_vector_line_token_cls: Type[Token] = Code20VectorLineToken
    macro_variable_definition_token_cls: Type[Token] = MacroVariableAssignment
    macro_variable_name_token_cls: Type[Token] = MacroVariableName
    mo_unit_mode_token_cls: Type[Token] = UnitMode
    step_repeat_begin_token_cls: Type[Token] = StepRepeatBegin
    step_repeat_end_token_cls: Type[Token] = StepRepeatEnd
    ta_aperture_attribute_token_cls: Type[Token] = ApertureAttribute
    td_delete_attribute_token_cls: Type[Token] = DeleteAttribute
    tf_file_attribute_token_cls: Type[Token] = FileAttribute
    to_object_attribute_token_cls: Type[Token] = ObjectAttribute


class GerberGrammarBuilder(GrammarBuilder):
    """Base class for all Gerber grammar builders."""

    options: GerberGrammarBuilderOptions

    def __init__(
        self,
        wrapper: Optional[TokenWrapper] = None,
        *,
        is_raw: bool = False,
        options: Optional[GerberGrammarBuilderOptions] = None,
    ) -> None:
        super().__init__(
            wrapper=wrapper,
            is_raw=is_raw,
            options=options if options is not None else GerberGrammarBuilderOptions(),
        )

    def build(self) -> GerberGrammar:
        """Build grammar object."""
        wrapper = self.wrapper
        eoex = self._build_eoex()

        load_commands = self._build_load_commands()
        # Sets the polarity of the whole image.
        ip = self._build_stmt(
            wrapper(
                self.options.ip_image_polarity_token_cls,
                Literal("IP") + oneOf("POS NEG").set_results_name("image_polarity"),
            ),
        )
        # End of file.
        m02 = wrapper(
            self.options.m02_end_of_file_token_cls,
            Literal("M02").set_name("End of file") + eoex,
        )
        # Optional stop.
        m01 = wrapper(
            self.options.m01_optional_stop_token_cls,
            Literal("M01").set_name("Optional stop") + eoex,
        )
        # Program stop.
        m00 = wrapper(
            self.options.m00_program_stop_token_cls,
            Literal("M00").set_name("Program stop") + eoex,
        )

        dnn = wrapper(
            self.options.dnn_select_aperture_token_cls,
            self._build_aperture_identifier() + eoex,
        )
        """Sets the current aperture to D code nn."""

        fs = self._build_format_specifier()
        # Sets the unit to mm or inch.
        mo = self._build_stmt(
            wrapper(
                self.options.mo_unit_mode_token_cls,
                Literal("MO")
                + oneOf("MM IN").set_results_name("unit").set_name("unit"),
            ),
        )

        # Open a step and repeat statement.
        sr = self._build_step_repeat()

        # Opens a block aperture statement and assigns its aperture number
        ab_open = self._build_stmt(
            wrapper(
                self.options.block_aperture_begin_token_cls,
                Literal("AB") + self._build_aperture_identifier(),
            ),
        )
        # Closes a block aperture statement.
        ab_close = self._build_stmt(
            wrapper(self.options.block_aperture_end_token_cls, Literal("AB")),
        )

        g_codes = self._build_g_codes()
        d_codes = self._build_d_codes()
        comment = self._build_comment_token()
        attributes = self._build_attribute_tokens()
        macro = self._build_macro_tokens()
        define_aperture = self._build_define_aperture()

        common = (
            mo
            | fs
            | macro
            | define_aperture
            | dnn
            | (d_codes + eoex)
            | (g_codes + d_codes + eoex)
            | (g_codes + eoex)
            | load_commands
            | ip
            | ab_open
            | ab_close
            | sr
            | attributes
            | m01
            | eoex
            | comment
        )

        invalid_token = self.wrapper(
            self.options.invalid_token_cls,
            Regex(".+").set_results_name("content"),
        )

        resilient = self.wrapper(
            self.options.ast_token_cls,
            (common | m02 | m00 | invalid_token)[0, ...],
        )
        expressions = self.wrapper(
            self.options.ast_token_cls,
            (common | m02 | m00)[0, ...],
        )
        grammar = self.wrapper(
            self.options.ast_token_cls,
            common[0, ...] + (m02 | m00),
        )

        return GerberGrammar(grammar, expressions, resilient)

    def _build_load_commands(self) -> ParserElement:
        wrapper = self.wrapper

        lm = self._build_stmt(
            wrapper(
                self.options.lm_load_mirroring_token_cls,
                Literal("LM") + oneOf("N XY Y X").set_results_name("mirroring"),
            ),
        )
        lp = self._build_stmt(
            wrapper(
                self.options.lp_load_polarity_token_cls,
                Literal("LP") + oneOf("C D").set_results_name("polarity"),
            ),
        )
        ls = self._build_stmt(
            wrapper(
                self.options.ls_load_scaling_token_cls,
                Literal("LS") + self._build_decimal("scaling"),
            ),
        )
        lr = self._build_stmt(
            wrapper(
                self.options.lr_load_rotation_token_cls,
                Literal("LR") + self._build_decimal("rotation"),
            ),
        )
        ln = self._build_stmt(
            wrapper(
                self.options.ln_load_name_token_cls,
                Literal("LN") + self._build_string(),
            ),
        )
        in_ = self._build_stmt(
            wrapper(
                self.options.in_image_name_token_cls,
                Literal("IN") + self._build_string(),
            ),
        )
        as_ = self._build_stmt(
            wrapper(
                self.options.as_axes_select_token_cls,
                Literal("AS") + oneOf("AXBY AYBX").set_results_name("correspondence"),
            ),
        )
        of = self._build_stmt(
            wrapper(
                self.options.of_image_offset_token_cls,
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
                self.options.fs_coordinate_format_token_cls,
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
                self.options.step_repeat_begin_token_cls,
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
        sr_close = self._build_stmt(
            wrapper(self.options.step_repeat_end_token_cls, Literal("SR")),
        )

        return sr_open | sr_close

    def _build_g_codes(self) -> ParserElement:
        wrapper = self.wrapper

        g54dnn = wrapper(
            self.options.g54_select_aperture_token_cls,
            Regex("G0*54") + self._build_aperture_identifier(),
        )
        g01 = wrapper(self.options.g01_set_linear_token_cls, Regex("G0*1"))
        g02 = wrapper(self.options.g02_set_clockwise_circular_token_cls, Regex("G0*2"))
        g03 = wrapper(
            self.options.g03_set_counterclockwise_circular_token_cls,
            Regex("G0*3"),
        )
        g36 = wrapper(self.options.g36_begin_region_token_cls, Regex("G0*36"))
        g37 = wrapper(self.options.g37_end_region_token_cls, Regex("G0*37"))
        g70 = wrapper(self.options.g70_set_unit_inch_token_cls, Regex("G0*70"))
        g71 = wrapper(self.options.g71_set_unit_mm_token_cls, Regex("G0*71"))
        g74 = wrapper(self.options.g74_single_quadrant_token_cls, Regex("G0*74"))
        g75 = wrapper(self.options.g75_multi_quadrant_token_cls, Regex("G0*75"))
        g90 = wrapper(
            self.options.g90_set_coordinate_absolute_token_cls,
            Regex("G0*90"),
        )
        g91 = wrapper(
            self.options.g91_set_coordinate_incremental_token_cls,
            Regex("G0*91"),
        )

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
            self.options.d01_draw_token_cls,
            ((Opt(xy) + Opt(ij) + Regex("D0*1")) | (xy + Opt(ij))),
        )
        d02 = wrapper(
            self.options.d02_move_token_cls,
            Opt(xy) + Regex("D0*2"),
        )
        d03 = wrapper(
            self.options.d03_flash_token_cls,
            Opt(xy) + Regex("D0*3"),
        )

        return d03 | d02 | d01

    def _build_comment_token(self) -> ParserElement:
        wrapper = self.wrapper
        eoex = self._build_eoex()

        # A human readable comment, does not affect the image.
        return wrapper(
            self.options.g04_comment_token_cls,
            Regex("G0*4") + Opt(self._build_string(), default="") + eoex,
        )

    def _build_define_aperture(self) -> ParserElement:
        wrapper = self.wrapper

        ad = Literal("AD").set_name("AD code")

        circle = wrapper(
            self.options.define_circle_token_cls,
            ad
            + self._build_aperture_identifier()
            + Literal("C").set_results_name("aperture_type")
            + ","
            + self._build_decimal("diameter")
            + Opt("X" + self._build_decimal("hole_diameter")),
        ).set_name("define aperture circle")

        rectangle = wrapper(
            self.options.define_rectangle_token_cls,
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
            self.options.define_obround_token_cls,
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
            self.options.define_polygon_token_cls,
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
            self.options.define_macro_token_cls,
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
                    self.options.macro_begin_token_cls,
                    Literal("AM") + self._build_name("macro_name"),
                ),
                "macro_begin",
            )
            + self._build_eoex()
        )

        # Defines a macro aperture template.
        return self._build_stmt(
            wrapper(
                self.options.macro_definition_token_cls,
                am_start + macro_body,
            ),
            eoex=False,
        ).set_name("macro definition")

    def _build_macro_variable_definition(self) -> ParserElement:
        return self.wrapper(
            self.options.macro_variable_definition_token_cls,
            self._build_macro_variable()
            + "="
            + self._build_macro_expr("value")
            + self._build_eoex(),
        )

    def _build_macro_primitive(self) -> ParserElement:
        cs = Suppress(Literal(",").set_name("comma"))
        primitive_comment = self.wrapper(
            self.options.macro_comment_token_cls,
            "0" + self._build_string(),
        )
        primitive_circle = self.wrapper(
            self.options.macro_primitive_circle_token_cls,
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
            self.options.macro_primitive_vector_line_token_cls,
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
            self.options.macro_primitive_center_line_token_cls,
            "21"  # Center Line
            + cs
            + self._build_macro_expr("exposure")  # Exposure
            + cs
            + self._build_macro_expr("width")  # Width
            + cs
            + self._build_macro_expr("height")  # height
            + cs
            + self._build_macro_expr("center_x")  # Center X
            + cs
            + self._build_macro_expr("center_y")  # Center Y
            + cs
            + self._build_macro_expr("rotation"),  # Rotation
        )
        primitive_outline = self.wrapper(
            self.options.macro_primitive_outline_token_cls,
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
            self.options.macro_primitive_polygon_token_cls,
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
            self.options.macro_primitive_thermal_token_cls,
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
            self.options.macro_point_token_cls,
            cs + self._build_macro_expr("x") + cs + self._build_macro_expr("y"),
        )

    _macro_expr: Optional[ParserElement] = None

    def _build_macro_expr(self, expr_name: str = "expr") -> ParserElement:
        macro_variable = self._build_macro_variable()
        numeric_constant = self.wrapper(
            self.options.macro_numeric_constant_token_cls,
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
                            self.options.macro_negation_operator_token_cls.new,
                        ),
                        (
                            Suppress("+"),
                            1,
                            OpAssoc.RIGHT,
                            self.options.macro_positive_operator_token_cls.new,
                        ),
                        (
                            Suppress("/"),
                            2,
                            OpAssoc.RIGHT,
                            self.options.macro_division_operator_token_cls.new,
                        ),
                        (
                            Suppress(oneOf("x X")),
                            2,
                            OpAssoc.RIGHT,
                            self.options.macro_multiplication_operator_token_cls.new,
                        ),
                        (
                            Suppress("-"),
                            2,
                            OpAssoc.RIGHT,
                            self.options.macro_subtraction_operator_token_cls.new,
                        ),
                        (
                            Suppress("+"),
                            2,
                            OpAssoc.RIGHT,
                            self.options.macro_addition_operator_token_cls.new,
                        ),
                    ],
                ),
            )

        expr = arithmetic_expression | factor

        return expr.set_results_name(expr_name).set_name(expr_name)

    def _build_macro_variable(self) -> ParserElement:
        return self.wrapper(
            self.options.macro_variable_name_token_cls,
            Regex(r"\$[0-9]*[1-9][0-9]*")("macro_variable_name"),
        )

    def _build_attribute_tokens(self) -> ParserElement:
        wrapper = self.wrapper

        file_attribute_name = self._build_name().set_name("file attribute name")
        aperture_attribute_name = self._build_name().set_name("aperture attribute name")
        object_attribute_name = self._build_name().set_name("object attribute name")

        comma = Literal(",")
        comma_with_field = comma + self._build_field()
        maybe_comma_or_maybe_comma_with_field = Opt(comma_with_field | comma)

        # Set a file attribute.
        tf = wrapper(
            self.options.tf_file_attribute_token_cls,
            Literal("TF")
            + file_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Add an aperture attribute to the dictionary or modify it.
        ta = wrapper(
            self.options.ta_aperture_attribute_token_cls,
            Literal("TA")
            + aperture_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Add an object attribute to the dictionary or modify it.
        to = wrapper(
            self.options.to_object_attribute_token_cls,
            Literal("TO")
            + object_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Delete one or all attributes in the dictionary.
        td = wrapper(
            self.options.td_delete_attribute_token_cls,
            Literal("TD")
            + Opt(
                file_attribute_name | aperture_attribute_name | object_attribute_name,
            ).set_results_name("attribute_name"),
        )

        # Set a file attribute.
        tf_comment = wrapper(
            self.options.tf_file_attribute_token_cls,
            Regex("G0*4")
            + Literal("#@!")
            + Literal("TF")
            + file_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Add an aperture attribute to the dictionary or modify it.
        ta_comment = wrapper(
            self.options.ta_aperture_attribute_token_cls,
            Regex("G0*4")
            + Literal("#@!")
            + Literal("TA")
            + aperture_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Add an object attribute to the dictionary or modify it.
        to_comment = wrapper(
            self.options.to_object_attribute_token_cls,
            Regex("G0*4")
            + Literal("#@!")
            + Literal("TO")
            + object_attribute_name.set_results_name("attribute_name")
            + maybe_comma_or_maybe_comma_with_field,
        )
        # Delete one or all attributes in the dictionary.
        td_comment = wrapper(
            self.options.td_delete_attribute_token_cls,
            Regex("G0*4")
            + Literal("#@!")
            + Literal("TD")
            + Opt(
                file_attribute_name | aperture_attribute_name | object_attribute_name,
            ).set_results_name("attribute_name"),
        )

        attrs = tf | ta | to | td
        comment_attrs = tf_comment | ta_comment | to_comment | td_comment

        return self._build_stmt(attrs) | comment_attrs

    _build_eoex_cache: Optional[ParserElement] = None

    def _build_eoex(self) -> ParserElement:
        if self._build_eoex_cache is None:
            self._build_eoex_cache = self.wrapper(
                self.options.end_of_expression_token_cls,
                Literal("*").set_name("end of expression"),
            )
        return self._build_eoex_cache

    def _build_stmt(
        self,
        expr: ParserElement,
        *,
        eoex: bool = True,
    ) -> ParserElement:
        begin_stmt = Literal("%")
        end_stmt = Literal("%")

        return self.wrapper(
            self.options.statement_token_cls,
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
        resilient_grammar: ParserElement,
    ) -> None:
        self.strict_grammar = strict_grammar
        self.expression_grammar = expression_grammar
        self.resilient_grammar = resilient_grammar
