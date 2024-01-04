"""Gerber AST parser, version 2, parsing context."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.command_buffer2 import CommandBuffer2
from pygerber.gerberx3.parser2.errors2 import (
    ApertureNotDefined2Error,
    ExitParsingProcess2Interrupt,
    MacroNotDefinedError,
    ReferencedNotInitializedBlockBufferError,
    RegionNotInitializedError,
    SkipTokenInterrupt,
)
from pygerber.gerberx3.parser2.parser2hooks import Parser2Hooks
from pygerber.gerberx3.parser2.state2 import State2
from pygerber.gerberx3.state_enums import AxisCorrespondence
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID

if TYPE_CHECKING:
    from decimal import Decimal

    from pygerber.gerberx3.math.vector_2d import Vector2D
    from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
    from pygerber.gerberx3.parser2.commands2.command2 import Command2
    from pygerber.gerberx3.parser2.ihooks import IHooks
    from pygerber.gerberx3.state_enums import DrawMode, Mirroring, Polarity, Unit
    from pygerber.gerberx3.tokenizer.tokens.bases.token import Token
    from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import CoordinateParser


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
        self.hooks: IHooks = (
            Parser2Hooks() if self.options.hooks is None else self.options.hooks
        )
        self.current_token: Optional[Token] = None

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

    def skip_token(self) -> NoReturn:
        """Skip this token."""
        raise SkipTokenInterrupt

    def halt_parser(self) -> NoReturn:
        """Halt parsing process."""
        raise ExitParsingProcess2Interrupt

    def get_hooks(self) -> IHooks:
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
        if self.get_is_aperture_block():
            self.first_block_command_buffer().add_command(__command)
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

    def get_is_step_and_repeat(self) -> bool:
        """Get is_step_and_repeat property value."""
        return self.get_state().get_is_step_and_repeat()

    def set_is_step_and_repeat(self, is_step_and_repeat: bool) -> None:  # noqa: FBT001
        """Set the is_step_and_repeat property value."""
        return self.set_state(
            self.get_state().set_is_step_and_repeat(is_step_and_repeat),
        )

    def get_is_multi_quadrant(self) -> bool:
        """Get is_aperture_block property value."""
        return self.get_is_multi_quadrant()

    def set_is_multi_quadrant(self, is_multi_quadrant: bool) -> None:  # noqa: FBT001
        """Set the is_aperture_block property value."""
        return self.set_state(
            self.get_state().set_is_multi_quadrant(is_multi_quadrant),
        )

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
        return self.get_state().get_current_aperture_id()

    def set_current_aperture_id(self, current_aperture: Optional[ApertureID]) -> None:
        """Set the current_aperture property value."""
        return self.set_state(
            self.get_state().set_current_aperture_id(current_aperture),
        )

    def get_file_attribute(self, key: str) -> Optional[str]:
        """Get file attributes property."""
        return self.get_state().get_file_attribute(key)

    def delete_file_attribute(self, key: str) -> None:
        """Get file attributes property."""
        return self.set_state(self.get_state().delete_file_attribute(key))

    def set_file_attribute(self, key: str, value: str) -> None:
        """Set file attributes property."""
        return self.set_state(self.get_state().set_file_attribute(key, value))

    def get_aperture(self, __key: ApertureID) -> Aperture2:
        """Get apertures property value."""
        try:
            return self.get_state().get_aperture(__key)
        except KeyError as e:
            raise ApertureNotDefined2Error(self.current_token) from e

    def set_aperture(self, __key: ApertureID, __value: Aperture2) -> None:
        """Set the apertures property value."""
        return self.set_state(self.get_state().set_aperture(__key, __value))

    def get_macro(self, __key: str) -> Any:
        """Get macro property value."""
        try:
            return self.get_state().get_macro(__key)
        except KeyError as e:
            raise MacroNotDefinedError(self.current_token) from e

    def set_macro(self, __key: str, __value: str) -> None:
        """Set the macro property value."""
        return self.set_state(self.get_state().set_macro(__key, __value))

    def get_current_aperture_mutable_proxy(
        self,
    ) -> Aperture2MutableProxy | EmptyAperture2MutableProxy:
        """Get current_aperture property value."""
        aperture_id = self.get_state().get_current_aperture_id()
        if aperture_id is not None:
            return Aperture2MutableProxy(
                context=self,
                aperture_id=aperture_id,
            )
        return EmptyAperture2MutableProxy()


class EmptyAperture2MutableProxy(FrozenGeneralModel):
    """Represents one of the `None``-cases for the `current_aperture` in
    `Parser2Context`.
    """

    def set_attribute(self, name: str, value: str) -> None:
        """Add an attribute to aperture."""


class Aperture2MutableProxy(EmptyAperture2MutableProxy):
    """Represents a proxy for an aperture in the Gerber file."""

    context: Parser2Context
    """Parser context."""

    aperture_id: ApertureID
    """The ID of the aperture."""

    def set_attribute(self, name: str, value: str) -> None:
        """Add an attribute to aperture."""
        aperture = self.context.get_aperture(self.aperture_id)
        if aperture is not None:
            self.context.set_aperture(
                self.aperture_id,
                aperture.set_attribute(name, value),
            )


class Parser2ContextOptions(FrozenGeneralModel):
    """Options for Parser2Context."""

    initial_state: Optional[State2] = Field(default=None)
    initial_main_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    initial_region_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    initial_block_command_buffer: Optional[CommandBuffer2] = Field(default=None)
    hooks: Optional[IHooks] = Field(default=None)
