"""Gerber AST parser, version 2, parsing context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, NoReturn, Optional, Type

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.parser2.apertures2.circle2 import NoCircle2
from pygerber.gerberx3.parser2.attributes2 import (
    ApertureAttributes,
    FileAttributes,
    ObjectAttributes,
)
from pygerber.gerberx3.parser2.command_buffer2 import CommandBuffer2
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotDefined2Error,
    ExitParsingProcess2Interrupt,
    MacroNotDefinedError,
    MacroNotInitializedError,
    ReferencedNotInitializedBlockBufferError,
    RegionNotInitializedError,
    SkipTokenInterrupt,
    StepAndRepeatNotInitializedError,
)
from pygerber.gerberx3.parser2.macro2.expressions2.binary2 import (
    Addition2,
    Division2,
    Multiplication2,
    Subtraction2,
)
from pygerber.gerberx3.parser2.macro2.expressions2.constant2 import Constant2
from pygerber.gerberx3.parser2.macro2.expressions2.unary2 import Negation2, Positive2
from pygerber.gerberx3.parser2.macro2.expressions2.variable_name import VariableName2
from pygerber.gerberx3.parser2.macro2.macro2 import ApertureMacro2
from pygerber.gerberx3.parser2.macro2.statement_buffer2 import StatementBuffer2
from pygerber.gerberx3.parser2.parser2hooks import Parser2Hooks
from pygerber.gerberx3.parser2.parser2hooks_base import Parser2HooksBase
from pygerber.gerberx3.parser2.state2 import ApertureTransform, State2
from pygerber.gerberx3.state_enums import AxisCorrespondence
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.math.vector_2d import Vector2D
    from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
    from pygerber.gerberx3.parser2.commands2.command2 import Command2
    from pygerber.gerberx3.state_enums import DrawMode, Mirroring, Polarity, Unit
    from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
    from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import CoordinateParser


REGION_OUTLINE_DEFAULT_APERTURE_ID = ApertureID("%*__REGION_OUTLINE_APERTURE__*%")


class Parser2Context:
    """Context used by Gerber AST parser, version 2."""

    def __init__(self, options: Parser2ContextOptions | None = None) -> None:
        self.options = Parser2ContextOptions() if options is None else options
        self.state: State2 = (
            State2()
            if self.options.initial_state is None
            else self.options.initial_state
        )
        self.main_command_buffer: CommandBuffer2 = (
            CommandBuffer2()
            if self.options.initial_main_command_buffer is None
            else self.options.initial_main_command_buffer
        )
        self.region_command_buffer: Optional[CommandBuffer2] = None
        self.block_command_buffer_stack: list[CommandBuffer2] = []
        self.block_state_stack: list[State2] = []
        self.step_and_repeat_command_buffer: Optional[CommandBuffer2] = None
        self.state_before_step_and_repeat: Optional[State2] = None
        self.macro_statement_buffer: Optional[StatementBuffer2] = None
        self.macro_eval_buffer: Optional[CommandBuffer2] = None
        self.macro_variable_buffer: dict[str, Decimal] = {}
        self.hooks: Parser2HooksBase = (
            Parser2Hooks() if self.options.hooks is None else self.options.hooks
        )
        self.current_token: Optional[Token] = None
        self.reached_program_stop: bool = False
        self.reached_optional_stop: bool = False
        self.reached_end_of_file: bool = False

        self.file_attributes = FileAttributes()
        self.aperture_attributes = ApertureAttributes()
        self.object_attributes = ObjectAttributes()

        self.macro_expressions = (
            Parser2ContextMacroExpressionFactories()
            if self.options.custom_macro_expression_factories is None
            else self.options.custom_macro_expression_factories
        )
        self.apertures: dict[ApertureID, Aperture2] = {
            REGION_OUTLINE_DEFAULT_APERTURE_ID: NoCircle2(
                identifier=REGION_OUTLINE_DEFAULT_APERTURE_ID,
                diameter=Offset.NULL,
                hole_diameter=None,
            ),
        }

    def push_block_command_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.block_command_buffer_stack.append(
            CommandBuffer2()
            if self.options.initial_block_command_buffer is None
            else self.options.initial_block_command_buffer.copy(),
        )

    def pop_block_command_buffer(self) -> CommandBuffer2:
        """Return latest block aperture command buffer and delete it from the stack."""
        if len(self.block_command_buffer_stack) == 0:
            raise ReferencedNotInitializedBlockBufferError(self.current_token)
        return self.block_command_buffer_stack.pop()

    def first_block_command_buffer(self) -> CommandBuffer2:
        """Return first (topmost) block aperture command buffer."""
        if len(self.block_command_buffer_stack) == 0:
            raise ReferencedNotInitializedBlockBufferError(self.current_token)
        return self.block_command_buffer_stack[-1]

    def push_block_state(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.block_state_stack.append(self.state)

    def pop_block_state(self) -> State2:
        """Return latest block aperture command buffer and delete it from the stack."""
        if len(self.block_state_stack) == 0:
            raise ReferencedNotInitializedBlockBufferError(self.current_token)
        return self.block_state_stack.pop()

    def set_region_command_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.region_command_buffer = (
            CommandBuffer2()
            if self.options.initial_region_command_buffer is None
            else self.options.initial_region_command_buffer.copy()
        )

    def unset_region_command_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.region_command_buffer = None

    def get_region_command_buffer(self) -> CommandBuffer2:
        """Return latest block aperture command buffer and delete it from the stack."""
        if self.region_command_buffer is None:
            raise RegionNotInitializedError(self.current_token)
        return self.region_command_buffer

    def set_step_and_repeat_command_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.step_and_repeat_command_buffer = (
            CommandBuffer2()
            if self.options.initial_region_command_buffer is None
            else self.options.initial_region_command_buffer.copy()
        )

    def unset_step_and_repeat_command_buffer(self) -> None:
        """Unset step and repeat command buffer."""
        self.step_and_repeat_command_buffer = None

    def get_step_and_repeat_command_buffer(self) -> CommandBuffer2:
        """Return step and repeat command buffer."""
        if self.step_and_repeat_command_buffer is None:
            raise StepAndRepeatNotInitializedError(self.current_token)
        return self.step_and_repeat_command_buffer

    def get_state_before_step_and_repeat(self) -> State2:
        """Return step and repeat command buffer."""
        if self.state_before_step_and_repeat is None:
            raise StepAndRepeatNotInitializedError(self.current_token)
        return self.state_before_step_and_repeat

    def unset_state_before_step_and_repeat(self) -> None:
        """Unset step and repeat command buffer."""
        self.state_before_step_and_repeat = None

    def set_state_before_step_and_repeat(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.state_before_step_and_repeat = self.state

    def reset_state_to_pre_step_and_repeat(self) -> None:
        """Set state to state before step and repeat."""
        self.set_state(self.get_state_before_step_and_repeat())

    def get_macro_statement_buffer(self) -> StatementBuffer2:
        """Return macro statement buffer."""
        if self.macro_statement_buffer is None:
            raise MacroNotInitializedError(self.current_token)
        return self.macro_statement_buffer

    def set_macro_statement_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.macro_statement_buffer = (
            StatementBuffer2()
            if self.options.initial_macro_statement_buffer is None
            else self.options.initial_macro_statement_buffer
        )

    def unset_macro_statement_buffer(self) -> None:
        """Unset step and repeat command buffer."""
        self.macro_statement_buffer = None

    def get_macro_eval_buffer(self) -> CommandBuffer2:
        """Return macro evaluation buffer."""
        if self.macro_eval_buffer is None:
            raise MacroNotInitializedError(self.current_token)
        return self.macro_eval_buffer

    def set_macro_eval_buffer(self) -> None:
        """Add new command buffer for block aperture draw commands."""
        self.macro_eval_buffer = (
            CommandBuffer2()
            if self.options.initial_macro_eval_buffer is None
            else self.options.initial_macro_eval_buffer
        )

    def unset_macro_eval_buffer(self) -> None:
        """Unset step and repeat command buffer."""
        self.macro_eval_buffer = None

    def skip_token(self) -> NoReturn:
        """Skip this token."""
        raise SkipTokenInterrupt

    def halt_parser(self) -> NoReturn:
        """Halt parsing process."""
        raise ExitParsingProcess2Interrupt

    def get_hooks(self) -> Parser2HooksBase:
        """Get hooks object."""
        return self.hooks

    def get_current_token(self) -> Optional[Token]:
        """Get current token object."""
        return self.current_token

    def set_current_token(self, token: Token) -> None:
        """Get current token object."""
        self.current_token = token

    def set_state(self, state: State2) -> None:
        """Set parser state."""
        self.state = state

    def add_command(self, __command: Command2) -> None:
        """Add draw command to command buffer."""
        if self.get_is_region():
            self.get_region_command_buffer().add_command(__command)
            return

        if self.get_is_aperture_block():
            self.first_block_command_buffer().add_command(__command)
            return

        if self.get_is_step_and_repeat():
            self.get_step_and_repeat_command_buffer().add_command(__command)
            return

        self.main_command_buffer.add_command(__command)

    def get_state(self) -> State2:
        """Get parser state."""
        return self.state

    def get_draw_units(self) -> Unit:
        """Get draw_units property value."""
        return self.get_state().get_draw_units()

    def set_draw_units(self, draw_units: Unit) -> None:
        """Set the draw_units property value."""
        return self.set_state(self.get_state().set_draw_units(draw_units))

    def get_coordinate_parser(self) -> CoordinateParser:
        """Get coordinate_parser property value."""
        return self.get_state().get_coordinate_parser()

    def set_coordinate_parser(self, coordinate_parser: CoordinateParser) -> None:
        """Set the coordinate_parser property value."""
        return self.set_state(
            self.get_state().set_coordinate_parser(coordinate_parser),
        )

    def get_polarity(self) -> Polarity:
        """Get polarity property value."""
        return self.get_state().get_polarity()

    def set_polarity(self, polarity: Polarity) -> None:
        """Set the polarity property value."""
        return self.set_state(self.get_state().set_polarity(polarity))

    def get_mirroring(self) -> Mirroring:
        """Get mirroring property value."""
        return self.get_state().get_mirroring()

    def set_mirroring(self, mirroring: Mirroring) -> None:
        """Set the mirroring property value."""
        return self.set_state(self.get_state().set_mirroring(mirroring))

    def get_rotation(self) -> Decimal:
        """Get rotation property value."""
        return self.get_state().get_rotation()

    def set_rotation(self, rotation: Decimal) -> None:
        """Set the rotation property value."""
        return self.set_state(self.get_state().set_rotation(rotation))

    def get_scaling(self) -> Decimal:
        """Get scaling property value."""
        return self.get_state().get_scaling()

    def set_scaling(self, scaling: Decimal) -> None:
        """Set the scaling property value."""
        return self.set_state(self.get_state().set_scaling(scaling))

    def get_is_output_image_negation_required(self) -> bool:
        """Get is_output_image_negation_required property value."""
        return self.get_state().get_is_output_image_negation_required()

    def set_is_output_image_negation_required(self, *, value: bool) -> None:
        """Set the is_output_image_negation_required property value."""
        return self.set_state(
            self.get_state().set_is_output_image_negation_required(value),
        )

    def get_image_name(self) -> Optional[str]:
        """Get image_name property value."""
        return self.get_state().get_image_name()

    def set_image_name(self, image_name: Optional[str]) -> None:
        """Set the image_name property value."""
        return self.set_state(self.get_state().set_image_name(image_name))

    def get_file_name(self) -> Optional[str]:
        """Get file_name property value."""
        return self.get_state().get_file_name()

    def set_file_name(self, file_name: Optional[str]) -> None:
        """Set the file_name property value."""
        return self.set_state(self.get_state().set_file_name(file_name))

    def get_axis_correspondence(self) -> AxisCorrespondence:
        """Get axis_correspondence property value."""
        return self.get_state().get_axis_correspondence()

    def set_axis_correspondence(self, axis_correspondence: AxisCorrespondence) -> None:
        """Set the axis_correspondence property value."""
        return self.set_state(
            self.get_state().set_axis_correspondence(axis_correspondence),
        )

    def get_draw_mode(self) -> DrawMode:
        """Get draw_mode property value."""
        return self.get_state().get_draw_mode()

    def set_draw_mode(self, draw_mode: DrawMode) -> None:
        """Set the draw_mode property value."""
        return self.set_state(self.get_state().set_draw_mode(draw_mode))

    def get_is_region(self) -> bool:
        """Get is_region property value."""
        return self.get_state().get_is_region()

    def set_is_region(self, is_region: bool) -> None:  # noqa: FBT001
        """Set the is_region property value."""
        return self.set_state(self.get_state().set_is_region(is_region))

    def get_is_aperture_block(self) -> bool:
        """Get is_aperture_block property value."""
        return self.get_state().get_is_aperture_block()

    def set_is_aperture_block(self, is_aperture_block: bool) -> None:  # noqa: FBT001
        """Set the is_aperture_block property value."""
        return self.set_state(
            self.get_state().set_is_aperture_block(is_aperture_block),
        )

    def get_aperture_block_id(self) -> Optional[ApertureID]:
        """Get is_aperture_block property value."""
        return self.get_state().get_aperture_block_id()

    def set_aperture_block_id(self, aperture_block_id: Optional[ApertureID]) -> None:
        """Set the is_aperture_block property value."""
        return self.set_state(
            self.get_state().set_aperture_block_id(aperture_block_id),
        )

    def get_is_multi_quadrant(self) -> bool:
        """Get is_aperture_block property value."""
        return self.get_state().get_is_multi_quadrant()

    def set_is_multi_quadrant(self, is_multi_quadrant: bool) -> None:  # noqa: FBT001
        """Set the is_aperture_block property value."""
        return self.set_state(
            self.get_state().set_is_multi_quadrant(is_multi_quadrant),
        )

    def get_is_step_and_repeat(self) -> bool:
        """Get is_step_and_repeat property value."""
        return self.get_state().get_is_step_and_repeat()

    def set_is_step_and_repeat(self, is_step_and_repeat: bool) -> None:  # noqa: FBT001
        """Set the is_step_and_repeat property value."""
        return self.set_state(
            self.get_state().set_is_step_and_repeat(is_step_and_repeat),
        )

    def get_x_repeat(self) -> int:
        """Get x_step property value."""
        return self.get_state().get_x_repeat()

    def set_x_repeat(self, x_repeat: int) -> None:
        """Set the x_repeat property value."""
        return self.set_state(self.get_state().set_x_repeat(x_repeat))

    def get_y_repeat(self) -> int:
        """Get y_step property value."""
        return self.get_state().get_y_repeat()

    def set_y_repeat(self, y_repeat: int) -> None:
        """Set the y_repeat property value."""
        return self.set_state(self.get_state().set_y_repeat(y_repeat))

    def get_x_step(self) -> Offset:
        """Get x_step property value."""
        return self.get_state().get_x_step()

    def set_x_step(self, x_step: Offset) -> None:
        """Set the x_step property value."""
        return self.set_state(self.get_state().set_x_step(x_step))

    def get_y_step(self) -> Offset:
        """Get y_step property value."""
        return self.get_state().get_y_step()

    def set_y_step(self, y_step: Offset) -> None:
        """Set the y_step property value."""
        return self.set_state(self.get_state().set_y_step(y_step))

    def get_current_position(self) -> Vector2D:
        """Get current_position property value."""
        return self.get_state().get_current_position()

    def set_current_position(self, current_position: Vector2D) -> None:
        """Set the current_position property value."""
        return self.set_state(
            self.get_state().set_current_position(current_position),
        )

    def get_current_aperture_id(self) -> Optional[ApertureID]:
        """Get current_aperture property value."""
        current_aperture_id = self.get_state().get_current_aperture_id()
        if current_aperture_id is None and self.get_is_region():
            return REGION_OUTLINE_DEFAULT_APERTURE_ID

        return current_aperture_id

    def set_current_aperture_id(self, current_aperture: Optional[ApertureID]) -> None:
        """Set the current_aperture property value."""
        return self.set_state(
            self.get_state().set_current_aperture_id(current_aperture),
        )

    def get_aperture(
        self,
        __key: ApertureID,
        transform: ApertureTransform,
    ) -> Aperture2:
        """Get apertures property value."""
        key_with_transform = ApertureID(
            f"{__key}+{transform.get_transform_key()}",
        )
        transformed_aperture = self.apertures.get(key_with_transform)
        if transformed_aperture is None:
            # Retrieve aperture with no transform and create a transformed copy.
            # If transform is all default, no copy is made.
            aperture = self._get_aperture(__key)
            transformed_aperture = (
                aperture.get_mirrored(transform.mirroring)
                .get_rotated(transform.rotation)
                .get_scaled(transform.scaling)
            )
            self.set_aperture(key_with_transform, transformed_aperture)

        return transformed_aperture

    def _get_aperture(self, __key: ApertureID) -> Aperture2:
        try:
            aperture = self.apertures[__key]
        except KeyError as e:
            raise ApertureNotDefined2Error(self.current_token) from e
        return aperture

    def set_aperture(self, __key: ApertureID, __value: Aperture2) -> None:
        """Set the apertures property value."""
        self.apertures[__key] = __value

    def get_macro(self, __key: str) -> ApertureMacro2:
        """Get macro property value."""
        try:
            return self.get_state().get_macro(__key)
        except KeyError as e:
            raise MacroNotDefinedError(self.current_token) from e

    def set_macro(self, __key: str, __value: ApertureMacro2) -> None:
        """Set the macro property value."""
        return self.set_state(self.get_state().set_macro(__key, __value))

    def set_reached_program_stop(self) -> None:
        """Set flag indicating that M00 token was reached."""
        self.reached_program_stop = True

    def get_reached_program_stop(self) -> bool:
        """Get flag indicating that M00 token was reached."""
        return self.reached_program_stop

    def set_reached_optional_stop(self) -> None:
        """Set flag indicating that M01 token was reached."""
        self.reached_optional_stop = True

    def get_reached_optional_stop(self) -> bool:
        """Get flag indicating that M01 token was reached."""
        return self.reached_optional_stop

    def set_reached_end_of_file(self) -> None:
        """Set flag indicating that M02 end of file was reached."""
        self.reached_end_of_file = True

    def get_reached_end_of_file(self) -> bool:
        """Get flag indicating that M02 end of file was reached."""
        return self.reached_end_of_file

    def get_file_attribute(self, key: str) -> Optional[str]:
        """Get file attributes property."""
        return self.file_attributes.get(key)

    def delete_file_attribute(self, key: str) -> None:
        """Get file attributes property."""
        self.file_attributes = self.file_attributes.delete(key)

    def set_file_attribute(self, key: str, value: Optional[str]) -> None:
        """Set file attributes property."""
        self.file_attributes = self.file_attributes.update(key, value)

    def get_aperture_attribute(self, key: str) -> Optional[str]:
        """Get aperture attributes property."""
        return self.aperture_attributes.get(key)

    def delete_aperture_attribute(self, key: str) -> None:
        """Delete aperture attributes property."""
        self.aperture_attributes = self.aperture_attributes.delete(key)

    def clear_aperture_attributes(self) -> None:
        """Clear aperture attributes property."""
        self.aperture_attributes = ApertureAttributes()

    def set_aperture_attribute(self, key: str, value: Optional[str]) -> None:
        """Set aperture attributes property."""
        self.aperture_attributes = self.aperture_attributes.update(key, value)

    def get_object_attribute(self, key: str) -> Optional[str]:
        """Get object attributes property."""
        return self.object_attributes.get(key)

    def delete_object_attribute(self, key: str) -> None:
        """Delete object attributes property."""
        self.object_attributes = self.object_attributes.delete(key)

    def set_object_attribute(self, key: str, value: Optional[str]) -> None:
        """Set object attributes property."""
        self.object_attributes = self.object_attributes.update(key, value)

    def clear_object_attributes(self) -> None:
        """Clear object attributes property."""
        self.object_attributes = ObjectAttributes()


@dataclass
class Parser2ContextMacroExpressionFactories:
    """Collection of factories for all macro expressions."""

    constant: Type[Constant2] = Constant2
    variable_name: Type[VariableName2] = VariableName2
    addition: Type[Addition2] = Addition2
    subtraction: Type[Subtraction2] = Subtraction2
    multiplication: Type[Multiplication2] = Multiplication2
    division: Type[Division2] = Division2
    negation: Type[Negation2] = Negation2
    positive: Type[Positive2] = Positive2


class Parser2ContextOptions(FrozenGeneralModel):
    """Options for Parser2Context."""

    initial_state: Optional[State2] = Field(default=None)
    initial_main_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    initial_region_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    initial_block_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    initial_macro_statement_buffer: Optional[StatementBuffer2] = Field(default=None)
    initial_macro_eval_buffer: Optional[CommandBuffer2] = Field(default=None)
    custom_macro_expression_factories: Optional[
        Parser2ContextMacroExpressionFactories
    ] = Field(
        default=None,
    )
    hooks: Optional[Parser2HooksBase] = Field(default=None)
