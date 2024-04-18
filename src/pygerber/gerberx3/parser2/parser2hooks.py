"""Implementation of hooks for Gerber AST Parser, version 2."""

# ruff: noqa: D401
from __future__ import annotations

import math
from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from pygerber.common.error import throw
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.apertures2.block2 import Block2
from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2, NoCircle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.command_buffer2 import CommandBuffer2
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2, CCArc2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotSelected2Error,
    IncrementalCoordinatesNotSupported2Error,
    NoValidArcCenterFoundError,
    StepAndRepeatNotInitializedError,
    UnnamedBlockApertureNotAllowedError,
)
from pygerber.gerberx3.parser2.macro2.assignment2 import Assignment2
from pygerber.gerberx3.parser2.macro2.macro2 import ApertureMacro2
from pygerber.gerberx3.parser2.macro2.point2 import Point2
from pygerber.gerberx3.parser2.macro2.primitives2.code_1_circle2 import Code1Circle2
from pygerber.gerberx3.parser2.macro2.primitives2.code_2_vector_line2 import (
    Code2VectorLine2,
)
from pygerber.gerberx3.parser2.macro2.primitives2.code_4_outline2 import Code4Outline2
from pygerber.gerberx3.parser2.macro2.primitives2.code_5_polygon2 import Code5Polygon2
from pygerber.gerberx3.parser2.macro2.primitives2.code_6_moire2 import Code6Moire2
from pygerber.gerberx3.parser2.macro2.primitives2.code_7_thermal2 import Code7Thermal2
from pygerber.gerberx3.parser2.macro2.primitives2.code_20_vector_line2 import (
    Code20VectorLine2,
)
from pygerber.gerberx3.parser2.macro2.primitives2.code_21_center_line2 import (
    Code21CenterLine2,
)
from pygerber.gerberx3.parser2.macro2.primitives2.code_22_lower_left_line2 import (
    Code22LowerLeftLine2,
)
from pygerber.gerberx3.parser2.parser2hooks_base import Parser2HooksBase
from pygerber.gerberx3.parser2.state2 import ApertureTransform
from pygerber.gerberx3.state_enums import (
    DrawMode,
    ImagePolarityEnum,
    Mirroring,
    Polarity,
    Unit,
)
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    CoordinateParser,
)

if TYPE_CHECKING:
    from pygerber.gerberx3.parser2.context2 import Parser2Context
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
    from pygerber.gerberx3.tokenizer.tokens.d01_draw import D01Draw
    from pygerber.gerberx3.tokenizer.tokens.d02_move import D02Move
    from pygerber.gerberx3.tokenizer.tokens.d03_flash import D03Flash
    from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import DNNSelectAperture
    from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
        CoordinateFormat,
    )
    from pygerber.gerberx3.tokenizer.tokens.g01_set_linear import SetLinear
    from pygerber.gerberx3.tokenizer.tokens.g02_set_clockwise_circular import (
        SetClockwiseCircular,
    )
    from pygerber.gerberx3.tokenizer.tokens.g03_set_counterclockwise_circular import (
        SetCounterclockwiseCircular,
    )
    from pygerber.gerberx3.tokenizer.tokens.g36_begin_region import BeginRegion
    from pygerber.gerberx3.tokenizer.tokens.g37_end_region import EndRegion
    from pygerber.gerberx3.tokenizer.tokens.g54_select_aperture import G54SelectAperture
    from pygerber.gerberx3.tokenizer.tokens.g70_set_unit_inch import SetUnitInch
    from pygerber.gerberx3.tokenizer.tokens.g71_set_unit_mm import SetUnitMillimeters
    from pygerber.gerberx3.tokenizer.tokens.g74_single_quadrant import (
        SetSingleQuadrantMode,
    )
    from pygerber.gerberx3.tokenizer.tokens.g75_multi_quadrant import (
        SetMultiQuadrantMode,
    )
    from pygerber.gerberx3.tokenizer.tokens.g90_set_coordinate_absolute import (
        SetAbsoluteNotation,
    )
    from pygerber.gerberx3.tokenizer.tokens.g91_set_coordinate_incremental import (
        SetIncrementalNotation,
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
    from pygerber.gerberx3.tokenizer.tokens.macro.macro_begin import MacroBegin
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_1_circle import (
        Code1CircleToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_2_vector_line import (
        Code2VectorLineToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_4_outline import (
        Code4OutlineToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_5_polygon import (
        Code5PolygonToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_6_moire import (
        Code6MoireToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_7_thermal import (
        Code7ThermalToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_20_vector_line import (  # noqa: E501
        Code20VectorLineToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_21_center_line import (  # noqa: E501
        Code21CenterLineToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.code_22_lower_left_line import (  # noqa: E501
        Code22LowerLeftLineToken,
    )
    from pygerber.gerberx3.tokenizer.tokens.macro.statements.variable_assignment import (  # noqa: E501
        MacroVariableAssignment,
    )
    from pygerber.gerberx3.tokenizer.tokens.mo_unit_mode import UnitMode
    from pygerber.gerberx3.tokenizer.tokens.sr_step_repeat import (
        StepRepeatBegin,
        StepRepeatEnd,
    )
    from pygerber.gerberx3.tokenizer.tokens.ta_aperture_attribute import (
        ApertureAttribute,
    )
    from pygerber.gerberx3.tokenizer.tokens.td_delete_attribute import DeleteAttribute
    from pygerber.gerberx3.tokenizer.tokens.tf_file_attribute import FileAttribute
    from pygerber.gerberx3.tokenizer.tokens.to_object_attribute import ObjectAttribute

MAX_SINGLE_QUADRANT_ANGLE = 91.0


class Parser2Hooks(Parser2HooksBase):
    """Implementation of hooks for Gerber AST Parser, version 2."""

    class MacroBeginTokenHooks(Parser2HooksBase.MacroBeginTokenHooks):
        """Hooks for visiting macro begin token (AM)."""

        def on_parser_visit_token(
            self,
            token: MacroBegin,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_macro_statement_buffer()
            return super().on_parser_visit_token(token, context)

    class MacroCode1CircleTokenHooks(Parser2HooksBase.MacroCode1CircleTokenHooks):
        """Hooks for visiting macro primitive code 0 circle."""

        def on_parser_visit_token(
            self,
            token: Code1CircleToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code1Circle2(
                    exposure=token.exposure.to_parser2_expression(context),
                    diameter=token.diameter.to_parser2_expression(context),
                    center_x=token.center_x.to_parser2_expression(context),
                    center_y=token.center_y.to_parser2_expression(context),
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode2VectorLineTokenHooks(
        Parser2HooksBase.MacroCode2VectorLineTokenHooks,
    ):
        """Hooks for visiting macro primitive code 2 vector line."""

        def on_parser_visit_token(
            self,
            token: Code2VectorLineToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: Code2VectorLine
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code2VectorLine2(),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode4OutlineTokenHooks(Parser2HooksBase.MacroCode4OutlineTokenHooks):
        """Hooks for visiting macro primitive code 4 outline."""

        def on_parser_visit_token(
            self,
            token: Code4OutlineToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code4Outline2(
                    exposure=token.exposure.to_parser2_expression(context),
                    vertex_count=token.number_of_vertices.to_parser2_expression(
                        context,
                    ),
                    start_x=token.start_x.to_parser2_expression(context),
                    start_y=token.start_y.to_parser2_expression(context),
                    points=[point.to_parser2_point2(context) for point in token.point],
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode5PolygonTokenHooks(Parser2HooksBase.MacroCode5PolygonTokenHooks):
        """Hooks for visiting macro primitive code 5 polygon."""

        def on_parser_visit_token(
            self,
            token: Code5PolygonToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code5Polygon2(
                    exposure=token.exposure.to_parser2_expression(context),
                    number_of_vertices=token.number_of_vertices.to_parser2_expression(
                        context,
                    ),
                    center_x=token.center_x.to_parser2_expression(context),
                    center_y=token.center_y.to_parser2_expression(context),
                    diameter=token.diameter.to_parser2_expression(context),
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode6MoireTokenHooks(Parser2HooksBase.MacroCode6MoireTokenHooks):
        """Hooks for visiting macro primitive code 6 moire."""

        def on_parser_visit_token(
            self,
            token: Code6MoireToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code6Moire2(),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode7ThermalTokenHooks(Parser2HooksBase.MacroCode7ThermalTokenHooks):
        """Hooks for visiting macro primitive code 7 thermal."""

        def on_parser_visit_token(
            self,
            token: Code7ThermalToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code7Thermal2(
                    center_x=token.center_x.to_parser2_expression(context),
                    center_y=token.center_y.to_parser2_expression(context),
                    outer_diameter=token.outer_diameter.to_parser2_expression(context),
                    inner_diameter=token.inner_diameter.to_parser2_expression(context),
                    gap=token.gap.to_parser2_expression(context),
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode20VectorLineTokenHooks(
        Parser2HooksBase.MacroCode20VectorLineTokenHooks,
    ):
        """Hooks for visiting macro primitive code 20 vector line."""

        def on_parser_visit_token(
            self,
            token: Code20VectorLineToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code20VectorLine2(
                    exposure=token.exposure.to_parser2_expression(context),
                    width=token.width.to_parser2_expression(context),
                    start_x=token.start_x.to_parser2_expression(context),
                    start_y=token.start_y.to_parser2_expression(context),
                    end_x=token.end_x.to_parser2_expression(context),
                    end_y=token.end_y.to_parser2_expression(context),
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode21CenterLineTokenHooks(
        Parser2HooksBase.MacroCode21CenterLineTokenHooks,
    ):
        """Hooks for visiting macro primitive code 21 center line."""

        def on_parser_visit_token(
            self,
            token: Code21CenterLineToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Code21CenterLine2(
                    exposure=token.exposure.to_parser2_expression(context),
                    width=token.width.to_parser2_expression(context),
                    height=token.height.to_parser2_expression(context),
                    center_x=token.center_x.to_parser2_expression(context),
                    center_y=token.center_y.to_parser2_expression(context),
                    rotation=token.rotation.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroCode22LowerLeftLineTokenHooks(
        Parser2HooksBase.MacroCode22LowerLeftLineTokenHooks,
    ):
        """Hooks for visiting macro primitive code 22 lower left line."""

        def on_parser_visit_token(
            self,
            token: Code22LowerLeftLineToken,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(Code22LowerLeftLine2())
            return super().on_parser_visit_token(token, context)

    class MacroVariableAssignment(Parser2HooksBase.MacroVariableAssignment):
        """Hooks for visiting macro variable assignment token."""

        def on_parser_visit_token(
            self,
            token: MacroVariableAssignment,
            context: Parser2Context,
        ) -> None:
            """Adds the primitive to the statement buffer.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.get_macro_statement_buffer().add_statement(
                Assignment2(
                    variable_name=token.variable.name,
                    value=token.value.to_parser2_expression(context),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class MacroDefinitionTokenHooks(Parser2HooksBase.MacroDefinitionTokenHooks):
        """Hooks for visiting macro definition token (AM)."""

        def on_parser_visit_token(
            self,
            token: MacroDefinition,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            stmt_buff = context.get_macro_statement_buffer()
            macro_name = token.macro_name

            context.set_macro(
                macro_name,
                ApertureMacro2(name=macro_name, statements=stmt_buff.get_readonly()),
            )
            context.unset_macro_statement_buffer()
            return super().on_parser_visit_token(token, context)

    class BeginBlockApertureTokenHooks(Parser2HooksBase.BeginBlockApertureTokenHooks):
        """Hooks for visiting begin block aperture token (AB)."""

        def on_parser_visit_token(
            self,
            token: BlockApertureBegin,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.push_block_command_buffer()
            # Save state from before block definition started.
            context.push_block_state()

            context.set_current_position(Vector2D.NULL)
            context.set_is_aperture_block(is_aperture_block=True)
            context.set_aperture_block_id(token.identifier)

            return super().on_parser_visit_token(token, context)

    class EndBlockApertureTokenHooks(Parser2HooksBase.EndBlockApertureTokenHooks):
        """Hooks for visiting end block aperture token (AB)."""

        def on_parser_visit_token(
            self,
            token: BlockApertureEnd,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            command_buffer = context.pop_block_command_buffer()
            identifier = context.get_aperture_block_id()
            if identifier is None:
                raise UnnamedBlockApertureNotAllowedError(token)

            context.set_aperture(
                identifier,
                Block2(
                    identifier=identifier,
                    attributes=context.aperture_attributes,
                    command_buffer=command_buffer.get_readonly(),
                ),
            )
            # Restore context state from before the block definition.
            context.set_state(context.pop_block_state())
            return super().on_parser_visit_token(token, context)

    class DefineApertureCircleTokenHooks(
        Parser2HooksBase.DefineApertureCircleTokenHooks,
    ):
        """Hooks for visiting circle aperture definition token (ADD)."""

        def on_parser_visit_token(
            self,
            token: DefineCircle,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            hole_diameter = (
                None
                if token.hole_diameter is None
                else Offset.new(token.hole_diameter, context.get_draw_units())
            )

            context.set_aperture(
                token.aperture_id,
                Circle2(
                    identifier=token.aperture_id,
                    attributes=context.aperture_attributes,
                    diameter=Offset.new(token.diameter, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineApertureRectangleTokenHooks(
        Parser2HooksBase.DefineApertureRectangleTokenHooks,
    ):
        """Hooks for visiting rectangle aperture definition token (ADD)."""

        def on_parser_visit_token(
            self,
            token: DefineRectangle,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            hole_diameter = (
                None
                if token.hole_diameter is None
                else Offset.new(token.hole_diameter, context.get_draw_units())
            )

            context.set_aperture(
                token.aperture_id,
                Rectangle2(
                    identifier=token.aperture_id,
                    attributes=context.aperture_attributes,
                    x_size=Offset.new(token.x_size, context.get_draw_units()),
                    y_size=Offset.new(token.y_size, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineApertureObroundTokenHooks(
        Parser2HooksBase.DefineApertureObroundTokenHooks,
    ):
        """Hooks for visiting obround aperture definition token (ADD)."""

        def on_parser_visit_token(
            self,
            token: DefineObround,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            hole_diameter = (
                None
                if token.hole_diameter is None
                else Offset.new(token.hole_diameter, context.get_draw_units())
            )

            context.set_aperture(
                token.aperture_id,
                Obround2(
                    identifier=token.aperture_id,
                    attributes=context.aperture_attributes,
                    x_size=Offset.new(token.x_size, context.get_draw_units()),
                    y_size=Offset.new(token.y_size, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineAperturePolygonTokenHooks(
        Parser2HooksBase.DefineAperturePolygonTokenHooks,
    ):
        """Hooks for visiting polygon aperture definition token (ADD)."""

        def on_parser_visit_token(
            self,
            token: DefinePolygon,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            hole_diameter = (
                None
                if token.hole_diameter is None
                else Offset.new(token.hole_diameter, context.get_draw_units())
            )
            rotation = Decimal("0.0") if token.rotation is None else token.rotation

            context.set_aperture(
                token.aperture_id,
                Polygon2(
                    identifier=token.aperture_id,
                    attributes=context.aperture_attributes,
                    outer_diameter=Offset.new(
                        token.outer_diameter,
                        context.get_draw_units(),
                    ),
                    number_vertices=token.number_of_vertices,
                    rotation=rotation,
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineApertureMacroTokenHooks(Parser2HooksBase.DefineApertureMacroTokenHooks):
        """Hooks for visiting macro aperture definition token (ADD)."""

        def on_parser_visit_token(
            self,
            token: DefineMacro,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            macro = context.get_macro(token.aperture_type)
            context.set_macro_eval_buffer()
            context.macro_variable_buffer = {
                f"${i}": Decimal(param) for i, param in enumerate(token.am_param, 1)
            }
            macro.on_parser2_eval_statement(context)

            context.set_aperture(
                token.aperture_id,
                Macro2(
                    identifier=token.aperture_id,
                    attributes=context.aperture_attributes,
                    command_buffer=context.get_macro_eval_buffer().get_readonly(),
                ),
            )

            context.unset_macro_eval_buffer()
            context.macro_variable_buffer = {}

            return super().on_parser_visit_token(token, context)

    class MacroEvalHooks:
        """Hooks called when evaluating macro aperture."""

        def __init__(self) -> None:
            self.macro_id_counter = 0

        def get_next_id(self) -> ApertureID:
            """Get next aperture id for macro."""
            next_id = ApertureID(self.macro_id_counter)
            self.macro_id_counter += 1
            return next_id

        def on_code_1_circle(
            self,
            context: Parser2Context,
            primitive: Code1Circle2,
        ) -> None:
            """Evaluate code 1 circle primitive."""
            exposure = primitive.exposure.on_parser2_eval_expression(context)
            polarity = (
                Polarity.Clear
                if math.isclose(exposure, Decimal("0.0"))
                else Polarity.Dark
            )
            context.get_macro_eval_buffer().add_command(
                Flash2(
                    transform=ApertureTransform(
                        polarity=polarity,
                        mirroring=Mirroring.NoMirroring,
                        rotation=Decimal("0.0"),
                        scaling=Decimal("1.0"),
                    ),
                    aperture=Circle2(
                        identifier=ApertureID(self.get_next_id()),
                        diameter=Offset.new(
                            primitive.diameter.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        hole_diameter=None,
                    ),
                    flash_point=Vector2D(
                        x=Offset.new(
                            primitive.center_x.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y=Offset.new(
                            primitive.center_y.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                    ),
                ),
            )

        def on_code_2_vector_line(
            self,
            context: Parser2Context,
            primitive: Code2VectorLine2,
        ) -> None:
            """Evaluate code 2 vector line primitive."""

        def on_code_4_outline(
            self,
            context: Parser2Context,
            primitive: Code4Outline2,
        ) -> None:
            """Evaluate code 4 outline primitive."""
            exposure = primitive.exposure.on_parser2_eval_expression(context)
            polarity = (
                Polarity.Clear
                if math.isclose(exposure, Decimal("0.0"))
                else Polarity.Dark
            )
            transform = ApertureTransform(
                polarity=polarity,
                mirroring=Mirroring.NoMirroring,
                rotation=Decimal("0.0"),
                scaling=Decimal("1.0"),
            )
            aperture = Circle2(
                identifier=ApertureID(self.get_next_id()),
                diameter=Offset.NULL,
                hole_diameter=None,
            )
            context.get_macro_eval_buffer().add_command(
                Region2(
                    transform=ApertureTransform(
                        polarity=polarity,
                        mirroring=Mirroring.NoMirroring,
                        rotation=Decimal("0.0"),
                        scaling=Decimal("1.0"),
                    ),
                    command_buffer=CommandBuffer2(
                        [
                            Line2(
                                transform=transform,
                                aperture=aperture,
                                start_point=Vector2D(
                                    x=Offset.new(
                                        start_point.x.on_parser2_eval_expression(
                                            context,
                                        ),
                                        context.get_draw_units(),
                                    ),
                                    y=Offset.new(
                                        start_point.y.on_parser2_eval_expression(
                                            context,
                                        ),
                                        context.get_draw_units(),
                                    ),
                                ),
                                end_point=Vector2D(
                                    x=Offset.new(
                                        end_point.x.on_parser2_eval_expression(
                                            context,
                                        ),
                                        context.get_draw_units(),
                                    ),
                                    y=Offset.new(
                                        end_point.y.on_parser2_eval_expression(
                                            context,
                                        ),
                                        context.get_draw_units(),
                                    ),
                                ),
                            )
                            for start_point, end_point in zip(
                                [
                                    Point2(x=primitive.start_x, y=primitive.start_y),
                                    *primitive.points,
                                ],
                                [
                                    *primitive.points,
                                    Point2(x=primitive.start_x, y=primitive.start_y),
                                ],
                            )
                        ],
                    ).get_readonly(),
                ).get_rotated(primitive.rotation.on_parser2_eval_expression(context)),
            )

        def on_code_5_polygon(
            self,
            context: Parser2Context,
            primitive: Code5Polygon2,
        ) -> None:
            """Evaluate code 5 polygon primitive."""
            exposure = primitive.exposure.on_parser2_eval_expression(context)
            polarity = (
                Polarity.Clear
                if math.isclose(exposure, Decimal("0.0"))
                else Polarity.Dark
            )
            context.get_macro_eval_buffer().add_command(
                Flash2(
                    transform=ApertureTransform(
                        polarity=polarity,
                        mirroring=Mirroring.NoMirroring,
                        rotation=Decimal("0.0"),
                        scaling=Decimal("1.0"),
                    ),
                    aperture=Polygon2(
                        identifier=ApertureID(self.get_next_id()),
                        outer_diameter=Offset.new(
                            primitive.diameter.on_parser2_eval_expression(
                                context,
                            ),
                        ),
                        number_vertices=round(
                            primitive.number_of_vertices.on_parser2_eval_expression(
                                context,
                            ),
                        ),
                        rotation=Decimal("0.0"),
                        hole_diameter=None,
                    ),
                    flash_point=Vector2D(
                        x=Offset.new(
                            primitive.center_x.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y=Offset.new(
                            primitive.center_y.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                    ),
                ).get_rotated(primitive.rotation.on_parser2_eval_expression(context)),
            )

        def on_code_6_moire(
            self,
            context: Parser2Context,
            primitive: Code6Moire2,
        ) -> None:
            """Evaluate code 6 moire primitive."""

        def on_code_7_thermal(
            self,
            context: Parser2Context,
            primitive: Code7Thermal2,
        ) -> None:
            """Evaluate code 7 thermal primitive."""

        def on_code_20_vector_line(
            self,
            context: Parser2Context,
            primitive: Code20VectorLine2,
        ) -> None:
            """Evaluate code 20 vector line primitive."""
            exposure = primitive.exposure.on_parser2_eval_expression(context)
            polarity = (
                Polarity.Clear
                if math.isclose(exposure, Decimal("0.0"))
                else Polarity.Dark
            )
            context.get_macro_eval_buffer().add_command(
                Line2(
                    transform=ApertureTransform(
                        polarity=polarity,
                        mirroring=Mirroring.NoMirroring,
                        rotation=Decimal("0.0"),
                        scaling=Decimal("1.0"),
                    ),
                    aperture=NoCircle2(
                        identifier=ApertureID(self.get_next_id()),
                        diameter=Offset.new(
                            primitive.width.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        hole_diameter=None,
                    ),
                    start_point=Vector2D(
                        x=Offset.new(
                            primitive.start_x.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y=Offset.new(
                            primitive.start_y.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                    ),
                    end_point=Vector2D(
                        x=Offset.new(
                            primitive.end_x.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y=Offset.new(
                            primitive.end_y.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                    ),
                ).get_rotated(primitive.rotation.on_parser2_eval_expression(context)),
            )

        def on_code_21_center_line(
            self,
            context: Parser2Context,
            primitive: Code21CenterLine2,
        ) -> None:
            """Evaluate code 21 center line primitive."""
            exposure = primitive.exposure.on_parser2_eval_expression(context)
            polarity = (
                Polarity.Clear
                if math.isclose(exposure, Decimal("0.0"))
                else Polarity.Dark
            )
            context.get_macro_eval_buffer().add_command(
                Flash2(
                    transform=ApertureTransform(
                        polarity=polarity,
                        mirroring=Mirroring.NoMirroring,
                        rotation=Decimal("0.0"),
                        scaling=Decimal("1.0"),
                    ),
                    aperture=Rectangle2(
                        identifier=ApertureID(self.get_next_id()),
                        x_size=Offset.new(
                            primitive.width.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y_size=Offset.new(
                            primitive.height.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        hole_diameter=None,
                    ),
                    flash_point=Vector2D(
                        x=Offset.new(
                            primitive.center_x.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                        y=Offset.new(
                            primitive.center_y.on_parser2_eval_expression(context),
                            context.get_draw_units(),
                        ),
                    ),
                ).get_rotated(primitive.rotation.on_parser2_eval_expression(context)),
            )

        def on_code_22_lower_left_line(
            self,
            context: Parser2Context,
            primitive: Code22LowerLeftLine2,
        ) -> None:
            """Evaluate code 22 lower left line primitive."""

        def on_assignment(
            self,
            context: Parser2Context,
            assignment: Assignment2,
        ) -> None:
            """Evaluate macro variable assignment statement."""
            context.macro_variable_buffer[assignment.variable_name] = (
                assignment.value.on_parser2_eval_expression(context)
            )

    class AxisSelectTokenHooksTokenHooks(
        Parser2HooksBase.AxisSelectTokenHooksTokenHooks,
    ):
        """Hooks for visiting axis select token (AS)."""

        def on_parser_visit_token(
            self,
            token: AxisSelect,
            context: Parser2Context,
        ) -> None:
            """Perform actions on the context implicated by this token.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context on which to perform the actions.

            """
            context.set_axis_correspondence(token.correspondence)
            return super().on_parser_visit_token(token, context)

    class CommandDrawTokenHooks(Parser2HooksBase.CommandDrawTokenHooks):
        """Hooks for visiting draw token (D01)."""

        def on_parser_visit_token(
            self,
            token: D01Draw,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            self.DRAW_MODE_DISPATCH_TABLE[context.get_draw_mode()](self, token, context)
            return super().on_parser_visit_token(token, context)

        def on_parser_visit_token_line(
            self,
            token: D01Draw,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            state = context.get_state()

            x = state.parse_coordinate(token.x)
            y = state.parse_coordinate(token.y)

            start_point = context.get_current_position()
            end_point = Vector2D(x=x, y=y)

            aperture_id = context.get_current_aperture_id() or throw(
                ApertureNotSelected2Error(token),
            )
            transform = context.get_state().get_aperture_transform()
            aperture = context.get_aperture(aperture_id, transform)

            command = Line2(
                attributes=context.object_attributes,
                aperture=aperture,
                start_point=start_point,
                end_point=end_point,
                transform=transform,
            ).get_mirrored(transform.get_mirroring())

            context.add_command(command)
            context.set_current_position(end_point)

        def on_parser_visit_token_arc(
            self,
            token: D01Draw,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            state = context.get_state()

            x = state.parse_coordinate(token.x)
            y = state.parse_coordinate(token.y)
            i = state.parse_coordinate(token.i)
            j = state.parse_coordinate(token.j)

            start_point = context.get_current_position()
            end_point = Vector2D(x=x, y=y)
            final_center_point = Vector2D.NULL

            if context.get_is_multi_quadrant() is False:
                # In single quadrant mode I and J offsets are unsigned, therefore we
                # need to check all 4 possible center points. We will choose first
                # valid, if anyone needs behavior strictly matching this from spec,
                # they can always create issue.
                for center_offset in (
                    Vector2D(x=i, y=j),
                    Vector2D(x=-i, y=j),
                    Vector2D(x=i, y=-j),
                    Vector2D(x=-i, y=-j),
                ):
                    center_point = start_point + center_offset
                    relative_start_point = start_point - center_point
                    relative_end_point = end_point - center_point
                    # Calculate radius of arc from center to start point and end point,
                    # If they aren't equal, this center candidate is not valid and we
                    # can skip it.
                    if not math.isclose(
                        relative_start_point.length().value,
                        relative_end_point.length().value,
                        rel_tol=1e-3,
                    ):
                        continue

                    # Calculate angle between vector pointing from center of arc to
                    # start, and vector pointing from center of arc to end point. If
                    # this angle is above 90 degrees, we exceeded allowed angle size in
                    # single quadrant mode and need to try other possible center points.
                    clockwise_angle = relative_start_point.angle_between(
                        relative_end_point,
                    )
                    if clockwise_angle > MAX_SINGLE_QUADRANT_ANGLE:
                        continue

                    final_center_point = center_point
                    break
                else:
                    raise NoValidArcCenterFoundError(token)

            else:
                # In multi quadrant mode I and J offsets are signed, so we can simply
                # use them to calculate center point relative to start point.
                center_offset = Vector2D(x=i, y=j)
                final_center_point = start_point + center_offset

            aperture_id = context.get_current_aperture_id() or throw(
                ApertureNotSelected2Error(token),
            )
            transform = context.get_state().get_aperture_transform()
            aperture = context.get_aperture(aperture_id, transform)
            command = Arc2(
                attributes=context.object_attributes,
                aperture=aperture,
                start_point=start_point,
                end_point=end_point,
                center_point=final_center_point,
                transform=context.get_state().get_aperture_transform(),
            ).get_mirrored(transform.get_mirroring())

            context.add_command(command)
            context.set_current_position(end_point)

        def on_parser_visit_token_cc_arc(
            self,
            token: D01Draw,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            state = context.get_state()

            x = state.parse_coordinate(token.x)
            y = state.parse_coordinate(token.y)
            i = state.parse_coordinate(token.i)
            j = state.parse_coordinate(token.j)

            start_point = context.get_current_position()
            end_point = Vector2D(x=x, y=y)
            final_center_point = Vector2D.NULL

            if context.get_is_multi_quadrant() is False:
                for center_offset in (
                    Vector2D(x=i, y=j),
                    Vector2D(x=-i, y=j),
                    Vector2D(x=i, y=-j),
                    Vector2D(x=-i, y=-j),
                ):
                    center_point = start_point + center_offset
                    relative_start_point = start_point - center_point
                    relative_end_point = end_point - center_point

                    if not math.isclose(
                        relative_start_point.length().value,
                        relative_end_point.length().value,
                        rel_tol=1e-6,
                    ):
                        continue

                    # Calculate angle between vector pointing from center of arc to
                    # start, and vector pointing from center of arc to end point. If
                    # this angle is above 90 degrees, we exceeded allowed angle size in
                    # single quadrant mode and need to try other possible center points.
                    clockwise_angle = relative_start_point.angle_between_cc(
                        relative_end_point,
                    )
                    if clockwise_angle > MAX_SINGLE_QUADRANT_ANGLE:
                        continue

                    final_center_point = center_point
                    break
                else:
                    raise NoValidArcCenterFoundError(token)

            else:
                center_offset = Vector2D(x=i, y=j)
                final_center_point = start_point + center_offset

            aperture_id = context.get_current_aperture_id() or throw(
                ApertureNotSelected2Error(token),
            )
            transform = context.get_state().get_aperture_transform()
            aperture = context.get_aperture(aperture_id, transform)
            command = CCArc2(
                attributes=context.object_attributes,
                aperture=aperture,
                start_point=start_point,
                end_point=end_point,
                center_point=final_center_point,
                transform=context.get_state().get_aperture_transform(),
            ).get_mirrored(transform.get_mirroring())

            context.add_command(command)
            context.set_current_position(end_point)

        DRAW_MODE_DISPATCH_TABLE = MappingProxyType(
            {
                DrawMode.Linear: on_parser_visit_token_line,
                DrawMode.ClockwiseCircular: on_parser_visit_token_arc,
                DrawMode.CounterclockwiseCircular: on_parser_visit_token_cc_arc,
            },
        )

    class CommandMoveTokenHooks(Parser2HooksBase.CommandMoveTokenHooks):
        """Hooks for visiting move token (D02)."""

        def on_parser_visit_token(
            self,
            token: D02Move,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            state = context.get_state()

            x = state.parse_coordinate(token.x)
            y = state.parse_coordinate(token.y)

            destination_point = Vector2D(x=x, y=y)

            context.set_current_position(destination_point)
            return super().on_parser_visit_token(token, context)

    class CommandFlashTokenHooks(Parser2HooksBase.CommandFlashTokenHooks):
        """Hooks for visiting flash token (D03)."""

        def on_parser_visit_token(
            self,
            token: D03Flash,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            state = context.get_state()

            x = state.parse_coordinate(token.x)
            y = state.parse_coordinate(token.y)

            flash_point = Vector2D(x=x, y=y)

            aperture_id = context.get_current_aperture_id() or throw(
                ApertureNotSelected2Error(token),
            )
            transform = context.get_state().get_aperture_transform()
            aperture = context.get_aperture(aperture_id, transform)

            if isinstance(aperture, Block2):
                cmd_buffer = aperture.command_buffer.get_transposed(flash_point)
                context.add_command(
                    BufferCommand2(
                        transform=transform,
                        command_buffer=cmd_buffer,
                    ),
                )

            else:
                context.add_command(
                    Flash2(
                        attributes=context.object_attributes,
                        aperture=aperture,
                        flash_point=flash_point,
                        transform=transform,
                    ),
                )

            context.set_current_position(flash_point)
            return super().on_parser_visit_token(token, context)

    class SelectApertureTokenHooks(Parser2HooksBase.SelectApertureTokenHooks):
        """Hooks for visiting select aperture token (DNN)."""

        def on_parser_visit_token(
            self,
            token: DNNSelectAperture,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_current_aperture_id(token.aperture_id)
            return super().on_parser_visit_token(token, context)

    class CoordinateFormatTokenHooks(Parser2HooksBase.CoordinateFormatTokenHooks):
        """Hooks for visiting coordinate format token (FS)."""

        def on_parser_visit_token(
            self,
            token: CoordinateFormat,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_coordinate_parser(
                CoordinateParser.new(
                    x_format=token.x_format,
                    y_format=token.y_format,
                    coordinate_mode=token.coordinate_mode,
                    zeros_mode=token.zeros_mode,
                ),
            )

    class SetLinearTokenHooks(Parser2HooksBase.SetLinearTokenHooks):
        """Hooks for visiting set linear token (G01)."""

        def on_parser_visit_token(
            self,
            token: SetLinear,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_mode(DrawMode.Linear)
            return super().on_parser_visit_token(token, context)

    class SetClockwiseCircularTokenHooks(
        Parser2HooksBase.SetClockwiseCircularTokenHooks,
    ):
        """Hooks for visiting set clockwise circular token (G02)."""

        def on_parser_visit_token(
            self,
            token: SetClockwiseCircular,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_mode(DrawMode.ClockwiseCircular)
            return super().on_parser_visit_token(token, context)

    class SetCounterClockwiseCircularTokenHooks(
        Parser2HooksBase.SetCounterClockwiseCircularTokenHooks,
    ):
        """Hooks for visiting set counter clockwise circular token (G03)."""

        def on_parser_visit_token(
            self,
            token: SetCounterclockwiseCircular,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_mode(DrawMode.CounterclockwiseCircular)
            return super().on_parser_visit_token(token, context)

    class CommentTokenHooks(Parser2HooksBase.CommentTokenHooks):
        """Hooks for visiting comment token (G04)."""

    class BeginRegionTokenHooks(Parser2HooksBase.BeginRegionTokenHooks):
        """Hooks for visiting begin region token (G36)."""

        def on_parser_visit_token(
            self,
            token: BeginRegion,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_is_region(is_region=True)
            context.set_region_command_buffer()

            return super().on_parser_visit_token(token, context)

    class EndRegionTokenHooks(Parser2HooksBase.EndRegionTokenHooks):
        """Hooks for visiting end region token (G37)."""

        def on_parser_visit_token(
            self,
            token: EndRegion,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_is_region(is_region=False)
            command_buffer = context.get_region_command_buffer()

            context.add_command(
                Region2(
                    aperture_attributes=context.aperture_attributes,
                    object_attributes=context.object_attributes,
                    command_buffer=command_buffer.get_readonly(),
                    transform=context.get_state().get_aperture_transform(),
                ),
            )

            context.unset_region_command_buffer()
            return super().on_parser_visit_token(token, context)

    class PrepareSelectApertureTokenHooks(
        Parser2HooksBase.PrepareSelectApertureTokenHooks,
    ):
        """Hooks for visiting prepare select aperture token (G54)."""

        def on_parser_visit_token(
            self,
            token: G54SelectAperture,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            self.hooks.select_aperture.on_parser_visit_token(token, context)
            return super().on_parser_visit_token(token, context)

    class SetUnitInchTokenHooks(Parser2HooksBase.SetUnitInchTokenHooks):
        """Hooks for visiting set unit inch token (G70)."""

        def on_parser_visit_token(
            self,
            token: SetUnitInch,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_units(Unit.Inches)
            return super().on_parser_visit_token(token, context)

    class SetUnitMillimetersTokenHooks(Parser2HooksBase.SetUnitMillimetersTokenHooks):
        """Hooks for visiting set unit millimeters token (G71)."""

        def on_parser_visit_token(
            self,
            token: SetUnitMillimeters,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_units(Unit.Millimeters)
            return super().on_parser_visit_token(token, context)

    class SetSingleQuadrantModeTokenHooks(
        Parser2HooksBase.SetSingleQuadrantModeTokenHooks,
    ):
        """Hooks for visiting set single-quadrant mode token (G74)."""

        def on_parser_visit_token(
            self,
            token: SetSingleQuadrantMode,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_is_multi_quadrant(is_multi_quadrant=False)
            return super().on_parser_visit_token(token, context)

    class SetMultiQuadrantModeTokenHooks(
        Parser2HooksBase.SetMultiQuadrantModeTokenHooks,
    ):
        """Hooks for visiting set multi-quadrant mode token (G75)."""

        def on_parser_visit_token(
            self,
            token: SetMultiQuadrantMode,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_is_multi_quadrant(is_multi_quadrant=True)
            return super().on_parser_visit_token(token, context)

    class SetCoordinateAbsoluteTokenHooks(
        Parser2HooksBase.SetCoordinateAbsoluteTokenHooks,
    ):
        """Hooks for visiting set coordinate absolute token (G90)."""

        def on_parser_visit_token(
            self,
            token: SetAbsoluteNotation,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            # NOOP - only absolute format supported.
            return super().on_parser_visit_token(token, context)

    class SetCoordinateIncrementalTokenHooks(
        Parser2HooksBase.SetCoordinateIncrementalTokenHooks,
    ):
        """Hooks for visiting set coordinate incremental token (G91)."""

        def on_parser_visit_token(
            self,
            token: SetIncrementalNotation,  # noqa: ARG002
            context: Parser2Context,  # noqa: ARG002
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            raise IncrementalCoordinatesNotSupported2Error

    class ImageNameTokenHooks(Parser2HooksBase.ImageNameTokenHooks):
        """Hooks for visiting image name token (IN)."""

        def on_parser_visit_token(
            self,
            token: ImageName,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_image_name(token.content)
            return super().on_parser_visit_token(token, context)

    class InvalidTokenHooks(Parser2HooksBase.InvalidTokenHooks):
        """Hooks for visiting invalid token."""

    class ImagePolarityTokenHooks(Parser2HooksBase.ImagePolarityTokenHooks):
        """Hooks for visiting image polarity token (IP)."""

        def on_parser_visit_token(
            self,
            token: ImagePolarity,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_is_output_image_negation_required(
                value=(token.image_polarity == ImagePolarityEnum.NEGATIVE),
            )
            return super().on_parser_visit_token(token, context)

    class LoadMirroringTokenHooks(Parser2HooksBase.LoadMirroringTokenHooks):
        """Hooks for visiting load mirroring token (LM)."""

        def on_parser_visit_token(
            self,
            token: LoadMirroring,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_mirroring(token.mirroring)
            return super().on_parser_visit_token(token, context)

    class LoadNameTokenHooks(Parser2HooksBase.LoadNameTokenHooks):
        """Hooks for visiting load name token (LN)."""

        def on_parser_visit_token(
            self,
            token: LoadName,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_file_name(token.content)
            return super().on_parser_visit_token(token, context)

    class LoadPolarityTokenHooks(Parser2HooksBase.LoadPolarityTokenHooks):
        """Hooks for visiting load polarity token (LP)."""

        def on_parser_visit_token(
            self,
            token: LoadPolarity,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_polarity(token.polarity)
            return super().on_parser_visit_token(token, context)

    class LoadRotationTokenHooks(Parser2HooksBase.LoadRotationTokenHooks):
        """Hooks for visiting load rotation token (LR)."""

        def on_parser_visit_token(
            self,
            token: LoadRotation,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_rotation(token.rotation)
            return super().on_parser_visit_token(token, context)

    class LoadScalingTokenHooks(Parser2HooksBase.LoadScalingTokenHooks):
        """Hooks for visiting load scaling token (LS)."""

        def on_parser_visit_token(
            self,
            token: LoadScaling,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_scaling(token.scaling)
            return super().on_parser_visit_token(token, context)

    class ProgramStopTokenHooks(Parser2HooksBase.ProgramStopTokenHooks):
        """Hooks for visiting program stop token (M00)."""

        def on_parser_visit_token(
            self,
            token: M00ProgramStop,  # noqa: ARG002
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_reached_program_stop()
            context.halt_parser()

    class OptionalStopTokenHooks(Parser2HooksBase.OptionalStopTokenHooks):
        """Hooks for visiting optional stop token (M01)."""

        def on_parser_visit_token(
            self,
            token: M01OptionalStop,  # noqa: ARG002
            context: Parser2Context,
        ) -> None:
            """Handle child parsing being completed."""
            context.set_reached_optional_stop()

    class EndOfFileTokenHooks(Parser2HooksBase.EndOfFileTokenHooks):
        """Hooks for visiting end of file token (M02)."""

        def on_parser_visit_token(
            self,
            token: M02EndOfFile,  # noqa: ARG002
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_reached_end_of_file()
            context.halt_parser()

    class UnitModeTokenHooks(Parser2HooksBase.UnitModeTokenHooks):
        """Hooks for visiting unit mode token (MO)."""

        def on_parser_visit_token(
            self,
            token: UnitMode,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_draw_units(token.unit)
            return super().on_parser_visit_token(token, context)

    class ImageOffsetTokenHooks(Parser2HooksBase.ImageOffsetTokenHooks):
        """Hooks for visiting image offset token (OF)."""

    class StepRepeatBeginTokenHooks(Parser2HooksBase.StepRepeatBeginTokenHooks):
        """Hooks for visiting step and repeat begin token (SR)."""

        def on_parser_visit_token(
            self,
            token: StepRepeatBegin,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_state_before_step_and_repeat()

            context.set_is_step_and_repeat(is_step_and_repeat=True)
            context.set_x_repeat(token.x_repeat)
            context.set_y_repeat(token.y_repeat)
            context.set_x_step(Offset.new(token.x_step, unit=context.get_draw_units()))
            context.set_y_step(Offset.new(token.y_step, unit=context.get_draw_units()))
            context.set_step_and_repeat_command_buffer()

            return super().on_parser_visit_token(token, context)

    class StepRepeatEndTokenHooks(Parser2HooksBase.StepRepeatEndTokenHooks):
        """Hooks for visiting step and repeat end token (SR)."""

        def on_parser_visit_token(
            self,
            token: StepRepeatEnd,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            if context.get_is_step_and_repeat() is False:
                raise StepAndRepeatNotInitializedError(token)

            command_buffer = context.get_step_and_repeat_command_buffer().get_readonly()
            commands: list[Command2] = []

            for x_index in range(context.get_x_repeat()):
                for y_index in range(context.get_y_repeat()):
                    buffer_command = BufferCommand2(
                        transform=context.get_state().get_aperture_transform(),
                        command_buffer=command_buffer,
                    ).get_transposed(
                        Vector2D(
                            x=(context.get_x_step() * x_index),
                            y=(context.get_y_step() * y_index),
                        ),
                    )
                    commands.append(buffer_command)

            # Resets all variables, including is_step_and_repeat and possibly other
            # set during recording of SR command block. Must be done before
            # add_command() to push SR command buffers to main command buffers.
            context.reset_state_to_pre_step_and_repeat()
            context.unset_state_before_step_and_repeat()
            context.unset_step_and_repeat_command_buffer()

            for command in commands:
                context.add_command(command)

            return super().on_parser_visit_token(token, context)

    class ApertureAttributeHooks(Parser2HooksBase.ApertureAttributeHooks):
        """Hooks for visiting aperture attribute token (TA)."""

        def on_parser_visit_token(
            self,
            token: ApertureAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_aperture_attribute(token.name, token.value)
            return super().on_parser_visit_token(token, context)

    class DeleteAttributeHooks(Parser2HooksBase.DeleteAttributeHooks):
        """Hooks for visiting delete attribute token (TD)."""

        def on_parser_visit_token(
            self,
            token: DeleteAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            if token.name is not None:
                context.delete_aperture_attribute(token.name)
                context.delete_object_attribute(token.name)
            else:
                context.clear_aperture_attributes()
                context.clear_object_attributes()
            return super().on_parser_visit_token(token, context)

    class FileAttributeHooks(Parser2HooksBase.FileAttributeHooks):
        """Hooks for visiting file attribute token (TF)."""

        def on_parser_visit_token(
            self,
            token: FileAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_file_attribute(token.name, token.value)
            return super().on_parser_visit_token(token, context)

    class ObjectAttributeHooks(Parser2HooksBase.ObjectAttributeHooks):
        """Hooks for visiting object attribute token (TO)."""

        def on_parser_visit_token(
            self,
            token: ObjectAttribute,
            context: Parser2Context,
        ) -> None:
            """Called when parser visits a token.

            This hook should perform all changes on context implicated by token type.

            Parameters
            ----------
            token: TokenT
                The token that is being visited.
            context : Parser2Context
                The context object containing information about the parser state.

            """
            context.set_object_attribute(token.name, token.value)
            return super().on_parser_visit_token(token, context)
