"""Implementation of hooks for Gerber AST Parser, version 2."""
# ruff: noqa: D401
from __future__ import annotations

import math
from decimal import Decimal
from types import MappingProxyType
from typing import TYPE_CHECKING

from pygerber.common.error import throw
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.apertures2.block2 import Block2
from pygerber.gerberx3.parser2.apertures2.circle2 import Circle2
from pygerber.gerberx3.parser2.apertures2.macro2 import Macro2
from pygerber.gerberx3.parser2.apertures2.obround2 import Obround2
from pygerber.gerberx3.parser2.apertures2.polygon2 import Polygon2
from pygerber.gerberx3.parser2.apertures2.rectangle2 import Rectangle2
from pygerber.gerberx3.parser2.commands2.arc2 import Arc2, CCArc2
from pygerber.gerberx3.parser2.commands2.buffer_command2 import BufferCommand2
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.parser2.commands2.flash2 import Flash2
from pygerber.gerberx3.parser2.commands2.line2 import Line2
from pygerber.gerberx3.parser2.commands2.region2 import Region2
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotSelected2Error,
    IncrementalCoordinatesNotSupported2Error,
    NestedRegionNotAllowedError,
    NoValidArcCenterFoundError,
    StepAndRepeatNotInitializedError,
    UnnamedBlockApertureNotAllowedError,
)
from pygerber.gerberx3.parser2.ihooks import IHooks
from pygerber.gerberx3.state_enums import DrawMode, ImagePolarityEnum, Unit
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
    from pygerber.gerberx3.tokenizer.tokens.mo_unit_mode import UnitMode
    from pygerber.gerberx3.tokenizer.tokens.sr_step_repeat import (
        StepRepeatBegin,
        StepRepeatEnd,
    )
    from pygerber.gerberx3.tokenizer.tokens.ta_aperture_attribute import (
        ApertureAttribute,
    )
    from pygerber.gerberx3.tokenizer.tokens.tf_file_attribute import FileAttribute
MAX_SINGLE_QUADRANT_ANGLE = 91.0


class Parser2Hooks(IHooks):
    """Implementation of hooks for Gerber AST Parser, version 2."""

    class MacroDefinitionTokenHooks(IHooks.MacroDefinitionTokenHooks):
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
            context.set_macro(token.macro_name, "Sentinel")
            return super().on_parser_visit_token(token, context)

    class BeginBlockApertureTokenHooks(IHooks.BeginBlockApertureTokenHooks):
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
            if context.get_is_aperture_block():
                raise NestedRegionNotAllowedError(token)

            context.push_block_command_buffer()
            context.set_is_aperture_block(is_aperture_block=True)
            context.set_aperture_block_id(token.identifier)
            return super().on_parser_visit_token(token, context)

    class EndBlockApertureTokenHooks(IHooks.EndBlockApertureTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
                    command_buffer=command_buffer.get_readonly(),
                ),
            )

            context.set_is_aperture_block(is_aperture_block=False)
            context.set_aperture_block_id(None)
            return super().on_parser_visit_token(token, context)

    class DefineApertureCircleTokenHooks(IHooks.DefineApertureCircleTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
                    diameter=Offset.new(token.diameter, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineApertureRectangleTokenHooks(IHooks.DefineApertureRectangleTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
                    x_size=Offset.new(token.x_size, context.get_draw_units()),
                    y_size=Offset.new(token.y_size, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineApertureObroundTokenHooks(IHooks.DefineApertureObroundTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
                    x_size=Offset.new(token.x_size, context.get_draw_units()),
                    y_size=Offset.new(token.y_size, context.get_draw_units()),
                    hole_diameter=hole_diameter,
                ),
            )
            return super().on_parser_visit_token(token, context)

    class DefineAperturePolygonTokenHooks(IHooks.DefineAperturePolygonTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
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

    class DefineApertureMacroTokenHooks(IHooks.DefineApertureMacroTokenHooks):
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
            context.get_macro(token.aperture_type)
            context.set_aperture(
                token.aperture_id,
                Macro2(
                    attributes=ImmutableMapping[str, str](),
                ),
            )
            return super().on_parser_visit_token(token, context)

    class AxisSelectTokenHooksTokenHooks(IHooks.AxisSelectTokenHooksTokenHooks):
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

    class CommandDrawTokenHooks(IHooks.CommandDrawTokenHooks):
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

            context.add_command(
                Line2(
                    attributes=ImmutableMapping[str, str](),
                    polarity=context.get_polarity(),
                    aperture_id=(
                        context.get_current_aperture_id()
                        or throw(ApertureNotSelected2Error(token))
                    ),
                    start_point=start_point,
                    end_point=end_point,
                    state=context.get_state().get_command2_proxy(),
                ),
            )
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

            context.add_command(
                Arc2(
                    attributes=ImmutableMapping[str, str](),
                    polarity=context.get_polarity(),
                    aperture_id=(
                        context.get_current_aperture_id()
                        or throw(ApertureNotSelected2Error(token))
                    ),
                    start_point=start_point,
                    end_point=end_point,
                    center_point=final_center_point,
                    state=context.get_state().get_command2_proxy(),
                ),
            )
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

            context.add_command(
                CCArc2(
                    attributes=ImmutableMapping[str, str](),
                    polarity=context.get_polarity(),
                    aperture_id=(
                        context.get_current_aperture_id()
                        or throw(ApertureNotSelected2Error(token))
                    ),
                    start_point=start_point,
                    end_point=end_point,
                    center_point=final_center_point,
                    state=context.get_state().get_command2_proxy(),
                ),
            )

            context.set_current_position(end_point)

        DRAW_MODE_DISPATCH_TABLE = MappingProxyType(
            {
                DrawMode.Linear: on_parser_visit_token_line,
                DrawMode.ClockwiseCircular: on_parser_visit_token_arc,
                DrawMode.CounterclockwiseCircular: on_parser_visit_token_cc_arc,
            },
        )

    class CommandMoveTokenHooks(IHooks.CommandMoveTokenHooks):
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

    class CommandFlashTokenHooks(IHooks.CommandFlashTokenHooks):
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

            context.add_command(
                Flash2(
                    attributes=ImmutableMapping[str, str](),
                    polarity=context.get_polarity(),
                    aperture_id=(
                        context.get_current_aperture_id()
                        or throw(ApertureNotSelected2Error(token))
                    ),
                    flash_point=flash_point,
                    state=context.get_state().get_command2_proxy(),
                ),
            )

            context.set_current_position(flash_point)
            return super().on_parser_visit_token(token, context)

    class SelectApertureTokenHooks(IHooks.SelectApertureTokenHooks):
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
            context.get_aperture(
                token.aperture_id,
            )  # Make sure aperture exists.
            context.set_current_aperture_id(token.aperture_id)
            return super().on_parser_visit_token(token, context)

    class CoordinateFormatTokenHooks(IHooks.CoordinateFormatTokenHooks):
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

    class SetLinearTokenHooks(IHooks.SetLinearTokenHooks):
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

    class SetClockwiseCircularTokenHooks(IHooks.SetClockwiseCircularTokenHooks):
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
        IHooks.SetCounterClockwiseCircularTokenHooks,
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

    class CommentTokenHooks(IHooks.CommentTokenHooks):
        """Hooks for visiting comment token (G04)."""

    class BeginRegionTokenHooks(IHooks.BeginRegionTokenHooks):
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

    class EndRegionTokenHooks(IHooks.EndRegionTokenHooks):
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
                    attributes=ImmutableMapping[str, str](),
                    polarity=context.get_polarity(),
                    command_buffer=command_buffer.get_readonly(),
                    state=context.get_state().get_command2_proxy(),
                ),
            )

            context.unset_region_command_buffer()
            return super().on_parser_visit_token(token, context)

    class PrepareSelectApertureTokenHooks(IHooks.PrepareSelectApertureTokenHooks):
        """Hooks for visiting prepare select aperture token (G54)."""

    class SetUnitInchTokenHooks(IHooks.SetUnitInchTokenHooks):
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

    class SetUnitMillimetersTokenHooks(IHooks.SetUnitMillimetersTokenHooks):
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

    class SetSingleQuadrantModeTokenHooks(IHooks.SetSingleQuadrantModeTokenHooks):
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

    class SetMultiQuadrantModeTokenHooks(IHooks.SetMultiQuadrantModeTokenHooks):
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

    class SetCoordinateAbsoluteTokenHooks(IHooks.SetCoordinateAbsoluteTokenHooks):
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

    class SetCoordinateIncrementalTokenHooks(IHooks.SetCoordinateIncrementalTokenHooks):
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

    class ImageNameTokenHooks(IHooks.ImageNameTokenHooks):
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

    class InvalidTokenHooks(IHooks.InvalidTokenHooks):
        """Hooks for visiting invalid token."""

    class ImagePolarityTokenHooks(IHooks.ImagePolarityTokenHooks):
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

    class LoadMirroringTokenHooks(IHooks.LoadMirroringTokenHooks):
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

    class LoadNameTokenHooks(IHooks.LoadNameTokenHooks):
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

    class LoadPolarityTokenHooks(IHooks.LoadPolarityTokenHooks):
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

    class LoadRotationTokenHooks(IHooks.LoadRotationTokenHooks):
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

    class LoadScalingTokenHooks(IHooks.LoadScalingTokenHooks):
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

    class ProgramStopTokenHooks(IHooks.ProgramStopTokenHooks):
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

    class OptionalStopTokenHooks(IHooks.OptionalStopTokenHooks):
        """Hooks for visiting optional stop token (M01)."""

        def on_parser_visit_token(
            self,
            token: M01OptionalStop,  # noqa: ARG002
            context: Parser2Context,
        ) -> None:
            """Handle child parsing being completed."""
            context.set_reached_optional_stop()

    class EndOfFileTokenHooks(IHooks.EndOfFileTokenHooks):
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

    class UnitModeTokenHooks(IHooks.UnitModeTokenHooks):
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

    class ImageOffsetTokenHooks(IHooks.ImageOffsetTokenHooks):
        """Hooks for visiting image offset token (OF)."""

    class StepRepeatBeginTokenHooks(IHooks.StepRepeatBeginTokenHooks):
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

    class StepRepeatEndTokenHooks(IHooks.StepRepeatEndTokenHooks):
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
                        attributes=ImmutableMapping[str, str](),
                        polarity=context.get_polarity(),
                        state=context.get_state().get_command2_proxy(),
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

    class ApertureAttributeHooks(IHooks.ApertureAttributeHooks):
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
            context.get_current_aperture_mutable_proxy().set_attribute(
                token.name,
                ",".join(token.value),
            )
            return super().on_parser_visit_token(token, context)

    class DeleteAttributeHooks(IHooks.DeleteAttributeHooks):
        """Hooks for visiting delete attribute token (TD)."""

    class FileAttributeHooks(IHooks.FileAttributeHooks):
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
            context.set_file_attribute(token.name, ",".join(token.value))
            return super().on_parser_visit_token(token, context)

    class ObjectAttributeHooks(IHooks.ObjectAttributeHooks):
        """Hooks for visiting object attribute token (TO)."""
