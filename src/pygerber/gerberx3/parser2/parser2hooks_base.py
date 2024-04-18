"""Parser hooks interface class, for Gerber AST parser, version 2."""

# ruff: noqa: D401
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar, Union

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    from pygerber.gerberx3.parser2.context2 import Parser2Context
    from pygerber.gerberx3.parser2.errors2 import Parser2Error
    from pygerber.gerberx3.parser2.macro2.assignment2 import Assignment2
    from pygerber.gerberx3.parser2.macro2.primitives2.code_1_circle2 import Code1Circle2
    from pygerber.gerberx3.parser2.macro2.primitives2.code_2_vector_line2 import (
        Code2VectorLine2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_4_outline2 import (
        Code4Outline2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_5_polygon2 import (
        Code5Polygon2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_6_moire2 import Code6Moire2
    from pygerber.gerberx3.parser2.macro2.primitives2.code_7_thermal2 import (
        Code7Thermal2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_20_vector_line2 import (
        Code20VectorLine2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_21_center_line2 import (
        Code21CenterLine2,
    )
    from pygerber.gerberx3.parser2.macro2.primitives2.code_22_lower_left_line2 import (
        Code22LowerLeftLine2,
    )
    from pygerber.gerberx3.parser2.parser2 import Parser2
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
    from pygerber.gerberx3.tokenizer.tokens.of_image_offset import ImageOffset
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


__all__ = ["TokenHooksBase", "Parser2HooksBase"]


BlockApertureEndT: TypeAlias = "BlockApertureEnd"
BlockApertureBeginT: TypeAlias = "BlockApertureBegin"
DefineCircleT: TypeAlias = "DefineCircle"
DefineRectangleT: TypeAlias = "DefineRectangle"
DefineObroundT: TypeAlias = "DefineObround"
DefinePolygonT: TypeAlias = "DefinePolygon"
DefineMacroT: TypeAlias = "DefineMacro"
DefineAnyT = Union[
    DefineCircleT,
    DefineRectangleT,
    DefineObroundT,
    DefinePolygonT,
    DefineMacroT,
]
AxisSelectT: TypeAlias = "AxisSelect"
D01DrawT: TypeAlias = "D01Draw"
D02MoveT: TypeAlias = "D02Move"
D03FlashT: TypeAlias = "D03Flash"
DNNSelectApertureT: TypeAlias = "DNNSelectAperture"
CoordinateFormatT: TypeAlias = "CoordinateFormat"
SetLinearT: TypeAlias = "SetLinear"
SetClockwiseCircularT: TypeAlias = "SetClockwiseCircular"
SetCounterclockwiseCircularT: TypeAlias = "SetCounterclockwiseCircular"
CommentT: TypeAlias = "Comment"
BeginRegionT: TypeAlias = "BeginRegion"
EndRegionT: TypeAlias = "EndRegion"
G54SelectApertureT: TypeAlias = "G54SelectAperture"
SetUnitInchT: TypeAlias = "SetUnitInch"
SetUnitMillimetersT: TypeAlias = "SetUnitMillimeters"
SetSingleQuadrantModeT: TypeAlias = "SetSingleQuadrantMode"
SetMultiQuadrantModeT: TypeAlias = "SetMultiQuadrantMode"
SetAbsoluteNotationT: TypeAlias = "SetAbsoluteNotation"
SetIncrementalNotationT: TypeAlias = "SetIncrementalNotation"
ImageNameT: TypeAlias = "ImageName"
InvalidTokenT: TypeAlias = "InvalidToken"
ImagePolarityT: TypeAlias = "ImagePolarity"
LoadMirroringT: TypeAlias = "LoadMirroring"
LoadNameT: TypeAlias = "LoadName"
LoadPolarityT: TypeAlias = "LoadPolarity"
LoadRotationT: TypeAlias = "LoadRotation"
LoadScalingT: TypeAlias = "LoadScaling"
M00ProgramStopT: TypeAlias = "M00ProgramStop"
M01OptionalStopT: TypeAlias = "M01OptionalStop"
M02EndOfFileT: TypeAlias = "M02EndOfFile"
MacroBeginT: TypeAlias = "MacroBegin"
Code1CircleTokenT: TypeAlias = "Code1CircleToken"
Code2VectorLineTokenT: TypeAlias = "Code2VectorLineToken"
Code4OutlineTokenT: TypeAlias = "Code4OutlineToken"
Code5PolygonTokenT: TypeAlias = "Code5PolygonToken"
Code6MoireTokenT: TypeAlias = "Code6MoireToken"
Code7ThermalTokenT: TypeAlias = "Code7ThermalToken"
Code20VectorLineTokenT: TypeAlias = "Code20VectorLineToken"
Code21CenterLineTokenT: TypeAlias = "Code21CenterLineToken"
Code22LowerLeftLineTokenT: TypeAlias = "Code22LowerLeftLineToken"
MacroVariableAssignmentT: TypeAlias = "MacroVariableAssignment"
MacroDefinitionT: TypeAlias = "MacroDefinition"
UnitModeT: TypeAlias = "UnitMode"
ImageOffsetT: TypeAlias = "ImageOffset"
StepRepeatBeginT: TypeAlias = "StepRepeatBegin"
StepRepeatEndT: TypeAlias = "StepRepeatEnd"
ApertureAttributeT: TypeAlias = "ApertureAttribute"
DeleteAttributeT: TypeAlias = "DeleteAttribute"
FileAttributeT: TypeAlias = "FileAttribute"
ObjectAttributeT: TypeAlias = "ObjectAttribute"


TokenT = TypeVar("TokenT")


class TokenHooksBase(Generic[TokenT]):
    """Class for creating token visit hooks."""

    def __init__(self, hooks: Parser2HooksBase) -> None:
        self.hooks = hooks

    def post_hooks_init(self) -> None:
        """Called after all hooks are assigned."""

    def pre_parser_visit_token(
        self,
        token: TokenT,
        context: Parser2Context,
    ) -> None:
        """Called before parser visits a token.

        Parameters
        ----------
        token: TokenT
            The token that will be visited.
        context : Parser2Context
            The context object containing information about the parser state.

        """

    def on_parser_visit_token(
        self,
        token: TokenT,
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

    def post_parser_visit_token(
        self,
        token: TokenT,
        context: Parser2Context,
    ) -> None:
        """Called after parser visits a token.

        Parameters
        ----------
        token: TokenT
            The token that was visited.
        context : Parser2Context
            The context object containing information about the parser state.

        """


class Parser2HooksBase:
    """Collection of overridable hooks for Gerber AST parser, version 2."""

    def __init__(self) -> None:  # noqa: PLR0915
        super().__init__()
        self.macro_begin = self.MacroBeginTokenHooks(self)
        self.macro_code_1_circle = self.MacroCode1CircleTokenHooks(self)
        self.macro_code_2_vector_line = self.MacroCode2VectorLineTokenHooks(self)
        self.macro_code_4_outline = self.MacroCode4OutlineTokenHooks(self)
        self.macro_code_5_polygon = self.MacroCode5PolygonTokenHooks(self)
        self.macro_code_6_moire = self.MacroCode6MoireTokenHooks(self)
        self.macro_code_7_thermal = self.MacroCode7ThermalTokenHooks(self)
        self.macro_code_20_vector_line = self.MacroCode20VectorLineTokenHooks(self)
        self.macro_code_21_center_line = self.MacroCode21CenterLineTokenHooks(self)
        self.macro_code_22_lower_left_line = self.MacroCode22LowerLeftLineTokenHooks(
            self,
        )
        self.macro_variable_assignment = self.MacroVariableAssignment(self)
        self.macro_definition = self.MacroDefinitionTokenHooks(self)
        self.macro_eval = self.MacroEvalHooks()

        self.end_block_aperture = self.EndBlockApertureTokenHooks(self)
        self.begin_block_aperture = self.BeginBlockApertureTokenHooks(self)

        self.define_circle_aperture = self.DefineApertureCircleTokenHooks(self)
        self.define_rectangle_aperture = self.DefineApertureRectangleTokenHooks(self)
        self.define_obround_aperture = self.DefineApertureObroundTokenHooks(self)
        self.define_polygon_aperture = self.DefineAperturePolygonTokenHooks(self)
        self.define_macro_aperture = self.DefineApertureMacroTokenHooks(self)
        self.define_aperture = self.DefineApertureTokenHooks(self)

        self.axis_select = self.AxisSelectTokenHooksTokenHooks(self)

        self.command_draw = self.CommandDrawTokenHooks(self)
        self.command_move = self.CommandMoveTokenHooks(self)
        self.command_flash = self.CommandFlashTokenHooks(self)

        self.select_aperture = self.SelectApertureTokenHooks(self)
        self.coordinate_format = self.CoordinateFormatTokenHooks(self)

        self.set_linear = self.SetLinearTokenHooks(self)
        self.set_clockwise_circular = self.SetClockwiseCircularTokenHooks(self)
        self.set_counter_clockwise_circular = (
            self.SetCounterClockwiseCircularTokenHooks(self)
        )

        self.comment = self.CommentTokenHooks(self)
        self.begin_region = self.BeginRegionTokenHooks(self)
        self.end_region = self.EndRegionTokenHooks(self)
        self.prepare_select_aperture = self.PrepareSelectApertureTokenHooks(self)
        self.set_unit_inch = self.SetUnitInchTokenHooks(self)
        self.set_unit_millimeters = self.SetUnitMillimetersTokenHooks(self)

        self.set_single_quadrant_mode = self.SetSingleQuadrantModeTokenHooks(self)
        self.set_multi_quadrant_mode = self.SetMultiQuadrantModeTokenHooks(self)

        self.set_coordinate_absolute = self.SetCoordinateAbsoluteTokenHooks(self)
        self.set_coordinate_incremental = self.SetCoordinateIncrementalTokenHooks(self)

        self.image_name = self.ImageNameTokenHooks(self)
        self.invalid_token = self.InvalidTokenHooks(self)
        self.image_polarity = self.ImagePolarityTokenHooks(self)
        self.load_name = self.LoadNameTokenHooks(self)

        self.load_mirroring = self.LoadMirroringTokenHooks(self)
        self.load_polarity = self.LoadPolarityTokenHooks(self)
        self.load_rotation = self.LoadRotationTokenHooks(self)
        self.load_scaling = self.LoadScalingTokenHooks(self)

        self.program_stop = self.ProgramStopTokenHooks(self)
        self.optional_stop = self.OptionalStopTokenHooks(self)
        self.end_of_file = self.EndOfFileTokenHooks(self)
        self.unit_mode = self.UnitModeTokenHooks(self)
        self.image_offset = self.ImageOffsetTokenHooks(self)

        self.step_repeat_begin = self.StepRepeatBeginTokenHooks(self)
        self.step_repeat_end = self.StepRepeatEndTokenHooks(self)

        self.aperture_attribute = self.ApertureAttributeHooks(self)
        self.delete_attribute = self.DeleteAttributeHooks(self)
        self.file_attribute = self.FileAttributeHooks(self)
        self.object_attribute = self.ObjectAttributeHooks(self)

        self._call_post_hooks_init()

    def _call_post_hooks_init(self) -> None:  # noqa: PLR0915
        self.macro_begin.post_hooks_init()
        self.macro_code_1_circle.post_hooks_init()
        self.macro_code_2_vector_line.post_hooks_init()
        self.macro_code_4_outline.post_hooks_init()
        self.macro_code_5_polygon.post_hooks_init()
        self.macro_code_6_moire.post_hooks_init()
        self.macro_code_7_thermal.post_hooks_init()
        self.macro_code_20_vector_line.post_hooks_init()
        self.macro_code_21_center_line.post_hooks_init()
        self.macro_code_22_lower_left_line.post_hooks_init()
        self.macro_variable_assignment.post_hooks_init()
        self.macro_definition.post_hooks_init()

        self.end_block_aperture.post_hooks_init()
        self.begin_block_aperture.post_hooks_init()

        self.define_circle_aperture.post_hooks_init()
        self.define_rectangle_aperture.post_hooks_init()
        self.define_obround_aperture.post_hooks_init()
        self.define_polygon_aperture.post_hooks_init()
        self.define_macro_aperture.post_hooks_init()
        self.define_aperture.post_hooks_init()

        self.axis_select.post_hooks_init()

        self.command_draw.post_hooks_init()
        self.command_move.post_hooks_init()
        self.command_flash.post_hooks_init()

        self.select_aperture.post_hooks_init()
        self.coordinate_format.post_hooks_init()

        self.set_linear.post_hooks_init()
        self.set_clockwise_circular.post_hooks_init()
        self.set_counter_clockwise_circular.post_hooks_init()

        self.comment.post_hooks_init()
        self.begin_region.post_hooks_init()
        self.end_region.post_hooks_init()
        self.prepare_select_aperture.post_hooks_init()

        self.set_unit_inch.post_hooks_init()
        self.set_unit_millimeters.post_hooks_init()

        self.set_single_quadrant_mode.post_hooks_init()
        self.set_multi_quadrant_mode.post_hooks_init()

        self.set_coordinate_absolute.post_hooks_init()
        self.set_coordinate_incremental.post_hooks_init()

        self.image_name.post_hooks_init()
        self.invalid_token.post_hooks_init()
        self.image_polarity.post_hooks_init()
        self.load_name.post_hooks_init()

        self.load_mirroring.post_hooks_init()
        self.load_polarity.post_hooks_init()
        self.load_rotation.post_hooks_init()
        self.load_scaling.post_hooks_init()

        self.program_stop.post_hooks_init()
        self.optional_stop.post_hooks_init()
        self.end_of_file.post_hooks_init()
        self.unit_mode.post_hooks_init()
        self.image_offset.post_hooks_init()

        self.step_repeat_begin.post_hooks_init()
        self.step_repeat_end.post_hooks_init()

        self.aperture_attribute.post_hooks_init()
        self.delete_attribute.post_hooks_init()
        self.file_attribute.post_hooks_init()
        self.object_attribute.post_hooks_init()

    def on_parser_init(self, parser: Parser2) -> None:
        """Called after parser initialization."""

    def pre_parse(self, context: Parser2Context) -> None:
        """Called before parsing starts."""

    def post_parse(self, context: Parser2Context) -> None:
        """Called after parsing finishes."""

    def on_parser_error(self, context: Parser2Context, error: Parser2Error) -> None:
        """Called when parsing error is thrown."""

    def on_other_error(self, context: Parser2Context, error: Exception) -> None:
        """Called when other error is thrown."""

    def pre_parser_visit_any_token(self, context: Parser2Context) -> None:
        """Called before parser visits any token."""

    def post_parser_visit_any_token(self, context: Parser2Context) -> None:
        """Called after parser visits any token."""

    class MacroBeginTokenHooks(TokenHooksBase[MacroBeginT]):
        """Hooks for visiting macro definition begin token (AM)."""

    class MacroCode1CircleTokenHooks(TokenHooksBase[Code1CircleTokenT]):
        """Hooks for visiting macro primitive code 0 circle."""

    class MacroCode2VectorLineTokenHooks(TokenHooksBase[Code2VectorLineTokenT]):
        """Hooks for visiting macro primitive code 2 vector line."""

    class MacroCode4OutlineTokenHooks(TokenHooksBase[Code4OutlineTokenT]):
        """Hooks for visiting macro primitive code 4 outline."""

    class MacroCode5PolygonTokenHooks(TokenHooksBase[Code5PolygonTokenT]):
        """Hooks for visiting macro primitive code 5 polygon."""

    class MacroCode6MoireTokenHooks(TokenHooksBase[Code6MoireTokenT]):
        """Hooks for visiting macro primitive code 6 moire."""

    class MacroCode7ThermalTokenHooks(TokenHooksBase[Code7ThermalTokenT]):
        """Hooks for visiting macro primitive code 7 thermal."""

    class MacroCode20VectorLineTokenHooks(TokenHooksBase[Code20VectorLineTokenT]):
        """Hooks for visiting macro primitive code 20 vector line."""

    class MacroCode21CenterLineTokenHooks(TokenHooksBase[Code21CenterLineTokenT]):
        """Hooks for visiting macro primitive code 21 center line."""

    class MacroCode22LowerLeftLineTokenHooks(TokenHooksBase[Code22LowerLeftLineTokenT]):
        """Hooks for visiting macro primitive code 22 lower left line."""

    class MacroVariableAssignment(TokenHooksBase[MacroVariableAssignmentT]):
        """Hooks for visiting macro variable assignment token."""

    class MacroDefinitionTokenHooks(TokenHooksBase[MacroDefinitionT]):
        """Hooks for visiting macro definition token (AM)."""

    class MacroEvalHooks:
        """Hooks called when evaluating macro aperture."""

        def on_code_1_circle(
            self,
            context: Parser2Context,
            primitive: Code1Circle2,
        ) -> None:
            """Evaluate code 1 circle primitive."""

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

        def on_code_5_polygon(
            self,
            context: Parser2Context,
            primitive: Code5Polygon2,
        ) -> None:
            """Evaluate code 5 polygon primitive."""

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

        def on_code_21_center_line(
            self,
            context: Parser2Context,
            primitive: Code21CenterLine2,
        ) -> None:
            """Evaluate code 21 center line primitive."""

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

    class BeginBlockApertureTokenHooks(TokenHooksBase[BlockApertureBeginT]):
        """Hooks for visiting begin block aperture token (AB)."""

    class EndBlockApertureTokenHooks(TokenHooksBase[BlockApertureEndT]):
        """Hooks for visiting end block aperture token (AB)."""

    class DefineApertureCircleTokenHooks(TokenHooksBase[DefineCircleT]):
        """Hooks for visiting circle aperture definition token (ADD)."""

    class DefineApertureRectangleTokenHooks(TokenHooksBase[DefineRectangleT]):
        """Hooks for visiting rectangle aperture definition token (ADD)."""

    class DefineApertureObroundTokenHooks(TokenHooksBase[DefineObroundT]):
        """Hooks for visiting obround aperture definition token (ADD)."""

    class DefineAperturePolygonTokenHooks(TokenHooksBase[DefinePolygonT]):
        """Hooks for visiting polygon aperture definition token (ADD)."""

    class DefineApertureMacroTokenHooks(TokenHooksBase[DefineMacroT]):
        """Hooks for visiting macro aperture definition token (ADD)."""

    class DefineApertureTokenHooks(TokenHooksBase[DefineAnyT]):
        """Hooks for visiting any aperture definition token (ADD)."""

    class AxisSelectTokenHooksTokenHooks(TokenHooksBase[AxisSelectT]):
        """Hooks for visiting axis select token (AS)."""

    class CommandDrawTokenHooks(TokenHooksBase[D01DrawT]):
        """Hooks for visiting draw token (D01)."""

    class CommandMoveTokenHooks(TokenHooksBase[D02MoveT]):
        """Hooks for visiting move token (D02)."""

    class CommandFlashTokenHooks(TokenHooksBase[D03FlashT]):
        """Hooks for visiting flash token (D03)."""

    class SelectApertureTokenHooks(TokenHooksBase[DNNSelectApertureT]):
        """Hooks for visiting select aperture token (DNN)."""

    class CoordinateFormatTokenHooks(TokenHooksBase[CoordinateFormatT]):
        """Hooks for visiting coordinate format token (FS)."""

    class SetLinearTokenHooks(TokenHooksBase[SetLinearT]):
        """Hooks for visiting set linear token (G01)."""

    class SetClockwiseCircularTokenHooks(TokenHooksBase[SetClockwiseCircularT]):
        """Hooks for visiting set clockwise circular token (G02)."""

    class SetCounterClockwiseCircularTokenHooks(
        TokenHooksBase[SetCounterclockwiseCircularT],
    ):
        """Hooks for visiting set counter clockwise circular token (G03)."""

    class CommentTokenHooks(TokenHooksBase[CommentT]):
        """Hooks for visiting comment token (G04)."""

    class BeginRegionTokenHooks(TokenHooksBase[BeginRegionT]):
        """Hooks for visiting begin region token (G36)."""

    class EndRegionTokenHooks(TokenHooksBase[EndRegionT]):
        """Hooks for visiting end region token (G37)."""

    class PrepareSelectApertureTokenHooks(TokenHooksBase[G54SelectApertureT]):
        """Hooks for visiting prepare select aperture token (G54)."""

    class SetUnitInchTokenHooks(TokenHooksBase[SetUnitInchT]):
        """Hooks for visiting set unit inch token (G70)."""

    class SetUnitMillimetersTokenHooks(TokenHooksBase[SetUnitMillimetersT]):
        """Hooks for visiting set unit millimeters token (G71)."""

    class SetSingleQuadrantModeTokenHooks(TokenHooksBase[SetSingleQuadrantModeT]):
        """Hooks for visiting set single-quadrant mode token (G74)."""

    class SetMultiQuadrantModeTokenHooks(TokenHooksBase[SetMultiQuadrantModeT]):
        """Hooks for visiting set multi-quadrant mode token (G75)."""

    class SetCoordinateAbsoluteTokenHooks(TokenHooksBase[SetAbsoluteNotationT]):
        """Hooks for visiting set coordinate absolute token (G90)."""

    class SetCoordinateIncrementalTokenHooks(TokenHooksBase[SetIncrementalNotationT]):
        """Hooks for visiting set coordinate incremental token (G91)."""

    class ImageNameTokenHooks(TokenHooksBase[ImageNameT]):
        """Hooks for visiting image name token (IN)."""

    class InvalidTokenHooks(TokenHooksBase[InvalidTokenT]):
        """Hooks for visiting invalid token."""

    class ImagePolarityTokenHooks(TokenHooksBase[ImagePolarityT]):
        """Hooks for visiting image polarity token (IP)."""

    class LoadMirroringTokenHooks(TokenHooksBase[LoadMirroringT]):
        """Hooks for visiting load mirroring token (LM)."""

    class LoadNameTokenHooks(TokenHooksBase[LoadNameT]):
        """Hooks for visiting load name token (LN)."""

    class LoadPolarityTokenHooks(TokenHooksBase[LoadPolarityT]):
        """Hooks for visiting load polarity token (LP)."""

    class LoadRotationTokenHooks(TokenHooksBase[LoadRotationT]):
        """Hooks for visiting load rotation token (LR)."""

    class LoadScalingTokenHooks(TokenHooksBase[LoadScalingT]):
        """Hooks for visiting load scaling token (LS)."""

    class ProgramStopTokenHooks(TokenHooksBase[M00ProgramStopT]):
        """Hooks for visiting program stop token (M00)."""

    class OptionalStopTokenHooks(TokenHooksBase[M01OptionalStopT]):
        """Hooks for visiting optional stop token (M01)."""

    class EndOfFileTokenHooks(TokenHooksBase[M02EndOfFileT]):
        """Hooks for visiting end of file token (M02)."""

    class UnitModeTokenHooks(TokenHooksBase[UnitModeT]):
        """Hooks for visiting unit mode token (MO)."""

    class ImageOffsetTokenHooks(TokenHooksBase[ImageOffsetT]):
        """Hooks for visiting image offset token (OF)."""

    class StepRepeatBeginTokenHooks(TokenHooksBase[StepRepeatBeginT]):
        """Hooks for visiting step and repeat begin token (SR)."""

    class StepRepeatEndTokenHooks(TokenHooksBase[StepRepeatEndT]):
        """Hooks for visiting step and repeat end token (SR)."""

    class ApertureAttributeHooks(TokenHooksBase[ApertureAttributeT]):
        """Hooks for visiting aperture attribute token (TA)."""

    class DeleteAttributeHooks(TokenHooksBase[DeleteAttributeT]):
        """Hooks for visiting delete attribute token (TD)."""

    class FileAttributeHooks(TokenHooksBase[FileAttributeT]):
        """Hooks for visiting file attribute token (TF)."""

    class ObjectAttributeHooks(TokenHooksBase[ObjectAttributeT]):
        """Hooks for visiting object attribute token (TO)."""
