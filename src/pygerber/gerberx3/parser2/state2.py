"""Alternative implementation of Gerber AST parser state, version 2.

Parser state is immutable and composed out of multiple sub objects. This approach allows
for cheap storage and updates of parser state, as whenever parser state is updated, only
one value must be changed, while rest of the structures remain unchanged and only
references to them are copied.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.immutable_map_model import ImmutableMapping
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.errors2 import (
    CoordinateFormatNotSet2Error,
    UnitNotSet2Error,
)
from pygerber.gerberx3.parser2.macro2.macro2 import ApertureMacro2
from pygerber.gerberx3.state_enums import (
    AxisCorrespondence,
    DrawMode,
    Mirroring,
    Polarity,
    Unit,
)
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    CoordinateParser,
)

if TYPE_CHECKING:
    from typing_extensions import Self


class State2Constants(FrozenGeneralModel):
    """Collection of rarely changing (usually once per AST) parser constants.

    This class represents the state constants used in the Gerber parser. It contains
    properties for various parser constants such as draw units, coordinate format,
    polarity, mirroring, rotation, scaling, image polarity, and file name. These
    constants are typically set once per AST (Abstract Syntax Tree) and are used
    throughout the parsing process.
    """

    draw_units: Optional[Unit] = Field(default=None)
    """The draw units used for the Gerber file. (Spec reference: 4.2.1)"""

    coordinate_parser: Optional[CoordinateParser] = Field(default=None)
    """The coordinate format specification, including the number of decimals.
    (Spec reference: 4.2.2)"""

    is_output_image_negation_required: bool = Field(default=False)
    """Flag indicating whether image polarity flipping is required.
    (Spec reference: 8.1.4)"""

    image_name: Optional[str] = Field(default=None)
    """The name of the image. (Spec reference: 8.1.3)"""

    file_name: Optional[str] = Field(default=None)
    """The name of the file. (Spec reference: 8.1.6)"""

    axis_correspondence: AxisCorrespondence = Field(default=AxisCorrespondence.AXBY)
    """Correspondence between the X, Y data axes and the A, B output device axes.
    It does not affect the image in computer to computer data exchange. It only
    has an effect how the image is positioned on an output device."""

    def get_draw_units(self) -> Unit:
        """Get the draw units.

        This method returns the draw units used for the Gerber file.

        Returns
        -------
        Unit
            The draw units.

        Raises
        ------
        UnitNotSet2Error
            If the draw units are not set.

        """
        if self.draw_units is None:
            raise UnitNotSet2Error
        return self.draw_units

    def set_draw_units(self, draw_units: Unit) -> Self:
        """Set the draw units for the state.

        This method updates the draw units of the state and returns a new instance of
        the state with the updated draw units.

        Parameters
        ----------
        draw_units : Unit
            The draw units to be set.

        Returns
        -------
        Self
            A new instance of the state with the updated draw units.

        """
        return self.model_copy(
            update={
                "draw_units": draw_units,
            },
        )

    def get_coordinate_parser(self) -> CoordinateParser:
        """Get coordinate_parser property value."""
        if self.coordinate_parser is None:
            raise CoordinateFormatNotSet2Error
        return self.coordinate_parser

    def set_coordinate_parser(self, coordinate_parser: CoordinateParser) -> Self:
        """Set the coordinate_parser property value."""
        return self.model_copy(
            update={
                "coordinate_parser": coordinate_parser,
            },
        )

    def get_is_output_image_negation_required(self) -> bool:
        """Get is_output_image_negation_required property value."""
        return self.is_output_image_negation_required

    def set_is_output_image_negation_required(
        self,
        value: bool,  # noqa: FBT001
    ) -> Self:
        """Set the is_output_image_negation_required property value."""
        return self.model_copy(
            update={
                "is_output_image_negation_required": value,
            },
        )

    def get_image_name(self) -> Optional[str]:
        """Get image_name property value."""
        return self.image_name

    def set_image_name(self, image_name: Optional[str]) -> Self:
        """Set the image_name property value."""
        return self.model_copy(
            update={
                "image_name": image_name,
            },
        )

    def get_file_name(self) -> Optional[str]:
        """Get file_name property value."""
        return self.file_name

    def set_file_name(self, file_name: Optional[str]) -> Self:
        """Set the file_name property value."""
        return self.model_copy(
            update={
                "file_name": file_name,
            },
        )

    def get_axis_correspondence(self) -> AxisCorrespondence:
        """Get token axis correspondence property value."""
        return self.axis_correspondence

    def set_axis_correspondence(self, axis_correspondence: AxisCorrespondence) -> Self:
        """Set token axis correspondence property value."""
        return self.model_copy(
            update={
                "axis_correspondence": axis_correspondence,
            },
        )


class ApertureTransform(FrozenGeneralModel):
    """Proxy for accessing Parser2State from the moment of creation of command."""

    polarity: Polarity = Field(default=Polarity.Dark)
    """The polarity object transformation parameter. (Spec reference: 4.9.2)"""

    mirroring: Mirroring = Field(default=Mirroring.NoMirroring)
    """The mirror object transformation parameter. (Spec reference: 4.9.3)"""

    rotation: Decimal = Field(default=Decimal("0.0"))
    """The rotation object transformation parameter. (Spec reference: 4.9.4)"""

    scaling: Decimal = Field(default=Decimal("1.0"))
    """The scale object transformation parameter. (Spec reference: 4.9.5)"""

    def get_polarity(self) -> Polarity:
        """Get polarity property value."""
        return self.polarity

    def set_polarity(self, polarity: Polarity) -> Self:
        """Set the polarity property value."""
        return self.model_copy(
            update={
                "polarity": polarity,
            },
        )

    def get_mirroring(self) -> Mirroring:
        """Get mirroring property value."""
        return self.mirroring

    def set_mirroring(self, mirroring: Mirroring) -> Self:
        """Set the mirroring property value."""
        return self.model_copy(
            update={
                "mirroring": mirroring,
            },
        )

    def get_rotation(self) -> Decimal:
        """Get rotation property value."""
        return self.rotation

    def set_rotation(self, rotation: Decimal) -> Self:
        """Set the rotation property value."""
        return self.model_copy(
            update={
                "rotation": rotation,
            },
        )

    def get_scaling(self) -> Decimal:
        """Get scaling property value."""
        return self.scaling

    def set_scaling(self, scaling: Decimal) -> Self:
        """Set the scaling property value."""
        return self.model_copy(
            update={
                "scaling": scaling,
            },
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of object scaled by factor."""
        return self.model_copy(
            update={
                "scaling": self.scaling * scale,
            },
        )

    def get_transform_key(self) -> str:
        """Get key describing rotation and scaling."""
        return (
            f"*%{self.get_rotation():.3f}*%{self.get_scaling():.3f}"
            f"*%{self.get_mirroring()}"
        )

    def has_mirroring_enabled(self) -> bool:
        """Check if there is any mirroring set."""
        return self.get_mirroring() is not Mirroring.NoMirroring


class State2MacroIndex(ImmutableMapping[str, ApertureMacro2]):
    """Index of all macros defined in Gerber AST until currently parsed token."""

    def set_macro(self, __id: str, __macro: ApertureMacro2) -> Self:
        """Add new macro to macros index."""
        # TODO(argmaster): Add warning handling.  # noqa: TD003
        return self.update(__id, __macro)

    def get_macro(self, __id: str) -> ApertureMacro2:
        """Get existing macro from index. When macro is missing KeyError is
        raised.
        """
        return self.mapping[__id]


class State2DrawFlags(FrozenGeneralModel):
    """Collection of drawing flags of Gerber AST parser, version 2.

    This class represents the drawing flags used in the Gerber AST parser.
    It contains properties to control various drawing modes and settings.
    """

    draw_mode: DrawMode = DrawMode.Linear
    """The current draw mode (linear, clockwise circular, or counterclockwise circular).
    """
    is_region: bool = False
    """Indicates whether the current statement is a region statement."""
    is_aperture_block: bool = False
    """Indicates whether the current statement is an aperture block statement."""
    aperture_block_id: Optional[ApertureID] = Field(default=None)
    """The ID of the current aperture block, if any."""
    is_multi_quadrant: bool = False
    """Indicates whether the multi-quadrant mode is enabled."""

    def get_draw_mode(self) -> DrawMode:
        """Get the current draw mode.

        Returns
        -------
            DrawMode: The current draw mode.

        """
        return self.draw_mode

    def set_draw_mode(self, draw_mode: DrawMode) -> State2DrawFlags:
        """Set the draw mode.

        Args:
        ----
            draw_mode (DrawMode): The new draw mode.

        Returns:
        -------
            State2DrawFlags: A new instance of State2DrawFlags with the updated draw
            mode.

        """
        return self.model_copy(
            update={
                "draw_mode": draw_mode,
            },
        )

    def get_is_region(self) -> bool:
        """Check if the current statement is a region statement.

        Returns
        -------
            bool: True if the current statement is a region statement, False otherwise.

        """
        return self.is_region

    def set_is_region(self, val: bool) -> State2DrawFlags:  # noqa: FBT001
        """Set the flag indicating whether the current statement is a region statement.

        Args:
        ----
            val (bool): True if the current statement is a region statement, False
            otherwise.

        Returns:
        -------
            State2DrawFlags: A new instance of State2DrawFlags with the updated flag.

        """
        return self.model_copy(
            update={
                "is_region": val,
            },
        )

    def get_is_aperture_block(self) -> bool:
        """Check if the current statement is an aperture block statement.

        Returns
        -------
            bool: True if the current statement is an aperture block statement, False
            otherwise.

        """
        return self.is_aperture_block

    def set_is_aperture_block(self, val: bool) -> State2DrawFlags:  # noqa: FBT001
        """Set the flag indicating whether the current statement is an aperture block
        statement.

        Args:
        ----
            val (bool): True if the current statement is an aperture block statement,
            False otherwise.

        Returns:
        -------
            State2DrawFlags: A new instance of State2DrawFlags with the updated flag.

        """
        return self.model_copy(
            update={
                "is_aperture_block": val,
            },
        )

    def get_aperture_block_id(self) -> Optional[ApertureID]:
        """Get the ID of the current aperture block.

        This method returns the ID of the current aperture block.

        Returns
        -------
        Optional[ApertureID]
            The ID of the current aperture block, or None if no aperture block is set.

        """
        return self.aperture_block_id

    def set_aperture_block_id(
        self,
        aperture_block_id: Optional[ApertureID],
    ) -> State2DrawFlags:
        """Set the ID of the current aperture block.

        This method sets the ID of the current aperture block.

        Parameters
        ----------
        aperture_block_id : Optional[ApertureID]
            The ID of the current aperture block.

        Returns
        -------
        State2DrawFlags
            A new instance of the State2DrawFlags with the updated flag.

        """
        return self.model_copy(
            update={
                "aperture_block_id": aperture_block_id,
            },
        )

    def get_is_multi_quadrant(self) -> bool:
        """Check if the multi-quadrant mode is enabled.

        Returns
        -------
            bool: True if the multi-quadrant mode is enabled, False otherwise.

        """
        return self.is_multi_quadrant

    def set_is_multi_quadrant(self, val: bool) -> Self:  # noqa: FBT001
        """Set the flag indicating whether the multi-quadrant mode is enabled.

        Args:
        ----
            val (bool): True to enable the multi-quadrant mode, False to disable it.

        Returns:
        -------
            State2DrawFlags: A new instance of State2DrawFlags with the updated flag.

        """
        return self.model_copy(
            update={
                "is_multi_quadrant": val,
            },
        )


class StepAndRepeatState2(FrozenGeneralModel):
    """Step and Repeat state maintainer."""

    is_step_and_repeat: bool = False
    """Indicates whether the current statement is a step and repeat statement."""

    x_repeat: int = 0
    """Number of repeats in the X direction."""

    y_repeat: int = 0
    """Number of repeats in the Y direction."""

    x_step: Offset = Offset.NULL
    """Step repeat distance in X direction."""

    y_step: Offset = Offset.NULL
    """Step repeat distance in Y direction."""

    def get_is_step_and_repeat(self) -> bool:
        """Check if the current statement is a step and repeat statement.

        Returns
        -------
            bool: True if the current statement is a step and repeat statement, False
            otherwise.

        """
        return self.is_step_and_repeat

    def set_is_step_and_repeat(self, val: bool) -> StepAndRepeatState2:  # noqa: FBT001
        """Set the flag indicating whether the current statement is a step and repeat
        statement.

        Args:
        ----
            val (bool): True if the current statement is a step and repeat statement,
            False otherwise.

        Returns:
        -------
            State2DrawFlags: A new instance of State2DrawFlags with the updated flag.

        """
        return self.model_copy(
            update={
                "is_step_and_repeat": val,
            },
        )

    def get_x_repeat(self) -> int:
        """Get x_repeat property value."""
        return self.x_repeat

    def set_x_repeat(self, val: int) -> StepAndRepeatState2:
        """Set the x_repeat property value."""
        return self.model_copy(
            update={
                "x_repeat": val,
            },
        )

    def get_y_repeat(self) -> int:
        """Get y_repeat property value."""
        return self.y_repeat

    def set_y_repeat(self, val: int) -> StepAndRepeatState2:
        """Set the y_repeat property value."""
        return self.model_copy(
            update={
                "y_repeat": val,
            },
        )

    def get_x_step(self) -> Offset:
        """Get x_step property value."""
        return self.x_step

    def set_x_step(self, val: Offset) -> StepAndRepeatState2:
        """Set the x_step property value."""
        return self.model_copy(
            update={
                "x_step": val,
            },
        )

    def get_y_step(self) -> Offset:
        """Get y_step property value."""
        return self.y_step

    def set_y_step(self, val: Offset) -> Self:
        """Set the y_step property value."""
        return self.model_copy(
            update={
                "y_step": val,
            },
        )


class State2(FrozenGeneralModel):
    """Gerber AST parser, version 2, parsing state.

    This object is immutable and intended way to update the state is through setters
    which return updated copy of state.
    """

    constants: State2Constants = Field(default_factory=State2Constants)
    """Collection of rarely changing Gerber state constants."""

    def get_constants(self) -> State2Constants:
        """Get constants property value."""
        return self.constants

    def set_constants(self, constants: State2Constants) -> Self:
        """Set the constants property value."""
        return self.model_copy(
            update={
                "constants": constants,
            },
        )

    def get_draw_units(self) -> Unit:
        """Get draw_units property value."""
        return self.get_constants().get_draw_units()

    def set_draw_units(self, draw_units: Unit) -> Self:
        """Set the draw_units property value."""
        return self.set_constants(self.get_constants().set_draw_units(draw_units))

    def get_coordinate_parser(self) -> CoordinateParser:
        """Get coordinate_parser property value."""
        return self.get_constants().get_coordinate_parser()

    def set_coordinate_parser(self, coordinate_parser: CoordinateParser) -> Self:
        """Set the coordinate_parser property value."""
        return self.set_constants(
            self.get_constants().set_coordinate_parser(coordinate_parser),
        )

    aperture_transform: ApertureTransform = Field(default_factory=ApertureTransform)

    def get_aperture_transform(self) -> ApertureTransform:
        """Get aperture_transform property value."""
        return self.aperture_transform

    def set_aperture_transform(self, aperture_transform: ApertureTransform) -> Self:
        """Set the aperture_transform property value."""
        return self.model_copy(
            update={
                "aperture_transform": aperture_transform,
            },
        )

    def get_polarity(self) -> Polarity:
        """Get polarity property value."""
        return self.get_aperture_transform().get_polarity()

    def set_polarity(self, polarity: Polarity) -> Self:
        """Set the polarity property value."""
        return self.set_aperture_transform(
            self.get_aperture_transform().set_polarity(polarity),
        )

    def get_mirroring(self) -> Mirroring:
        """Get mirroring property value."""
        return self.get_aperture_transform().get_mirroring()

    def set_mirroring(self, mirroring: Mirroring) -> Self:
        """Set the mirroring property value."""
        return self.set_aperture_transform(
            self.get_aperture_transform().set_mirroring(mirroring),
        )

    def get_rotation(self) -> Decimal:
        """Get rotation property value."""
        return self.get_aperture_transform().get_rotation()

    def set_rotation(self, rotation: Decimal) -> Self:
        """Set the rotation property value."""
        return self.set_aperture_transform(
            self.get_aperture_transform().set_rotation(rotation),
        )

    def get_scaling(self) -> Decimal:
        """Get scaling property value."""
        return self.get_aperture_transform().get_scaling()

    def set_scaling(self, scaling: Decimal) -> Self:
        """Set the scaling property value."""
        return self.set_aperture_transform(
            self.get_aperture_transform().set_scaling(scaling),
        )

    def get_is_output_image_negation_required(self) -> bool:
        """Get is_output_image_negation_required property value."""
        return self.get_constants().get_is_output_image_negation_required()

    def set_is_output_image_negation_required(
        self,
        value: bool,  # noqa: FBT001
    ) -> Self:
        """Set the is_output_image_negation_required property value."""
        return self.set_constants(
            self.get_constants().set_is_output_image_negation_required(value),
        )

    def get_image_name(self) -> Optional[str]:
        """Get image_name property value."""
        return self.get_constants().get_image_name()

    def set_image_name(self, image_name: Optional[str]) -> Self:
        """Set the image_name property value."""
        return self.set_constants(self.get_constants().set_image_name(image_name))

    def get_file_name(self) -> Optional[str]:
        """Get file_name property value."""
        return self.get_constants().get_file_name()

    def set_file_name(self, file_name: Optional[str]) -> Self:
        """Set the file_name property value."""
        return self.set_constants(self.get_constants().set_file_name(file_name))

    def get_axis_correspondence(self) -> AxisCorrespondence:
        """Get token axis correspondence property value."""
        return self.get_constants().get_axis_correspondence()

    def set_axis_correspondence(self, axis_correspondence: AxisCorrespondence) -> Self:
        """Set token axis correspondence property value."""
        return self.set_constants(
            self.get_constants().set_axis_correspondence(axis_correspondence),
        )

    flags: State2DrawFlags = Field(default_factory=State2DrawFlags)
    """Collection of more often changing Gerber state flags."""

    def get_flags(self) -> State2DrawFlags:
        """Get flags property value."""
        return self.flags

    def set_flags(self, flags: State2DrawFlags) -> Self:
        """Set the flags property value."""
        return self.model_copy(
            update={
                "flags": flags,
            },
        )

    def get_draw_mode(self) -> DrawMode:
        """Get draw_mode property value."""
        return self.get_flags().get_draw_mode()

    def set_draw_mode(self, draw_mode: DrawMode) -> Self:
        """Set the draw_mode property value."""
        return self.set_flags(self.get_flags().set_draw_mode(draw_mode))

    def get_is_region(self) -> bool:
        """Get is_region property value."""
        return self.get_flags().get_is_region()

    def set_is_region(self, is_region: bool) -> Self:  # noqa: FBT001
        """Set the is_region property value."""
        return self.set_flags(self.get_flags().set_is_region(is_region))

    def get_is_aperture_block(self) -> bool:
        """Get is_aperture_block property value."""
        return self.get_flags().get_is_aperture_block()

    def set_is_aperture_block(self, is_aperture_block: bool) -> Self:  # noqa: FBT001
        """Set the is_aperture_block property value."""
        return self.set_flags(
            self.get_flags().set_is_aperture_block(is_aperture_block),
        )

    def get_aperture_block_id(self) -> Optional[ApertureID]:
        """Get aperture_block_id property value."""
        return self.get_flags().get_aperture_block_id()

    def set_aperture_block_id(self, aperture_block_id: Optional[ApertureID]) -> Self:
        """Set the aperture_block_id property value."""
        return self.set_flags(
            self.get_flags().set_aperture_block_id(aperture_block_id),
        )

    def get_is_multi_quadrant(self) -> bool:
        """Get is_aperture_block property value."""
        return self.get_flags().get_is_multi_quadrant()

    def set_is_multi_quadrant(self, is_multi_quadrant: bool) -> Self:  # noqa: FBT001
        """Set the is_aperture_block property value."""
        return self.set_flags(
            self.get_flags().set_is_multi_quadrant(is_multi_quadrant),
        )

    step_repeat: StepAndRepeatState2 = Field(default_factory=StepAndRepeatState2)

    def get_step_and_repeat(self) -> StepAndRepeatState2:
        """Get step_repeat property value."""
        return self.step_repeat

    def set_step_and_repeat(self, step_and_repeat: StepAndRepeatState2) -> Self:
        """Set step_repeat property value."""
        return self.model_copy(
            update={
                "step_repeat": step_and_repeat,
            },
        )

    def get_is_step_and_repeat(self) -> bool:
        """Get is_step_and_repeat property value."""
        return self.get_step_and_repeat().get_is_step_and_repeat()

    def set_is_step_and_repeat(self, is_step_and_repeat: bool) -> Self:  # noqa: FBT001
        """Set the is_step_and_repeat property value."""
        return self.set_step_and_repeat(
            self.get_step_and_repeat().set_is_step_and_repeat(is_step_and_repeat),
        )

    def get_x_repeat(self) -> int:
        """Get x_repeat property value."""
        return self.get_step_and_repeat().get_x_repeat()

    def set_x_repeat(self, value: int) -> Self:
        """Set the x_repeat property value."""
        return self.set_step_and_repeat(
            self.get_step_and_repeat().set_x_repeat(value),
        )

    def get_y_repeat(self) -> int:
        """Get y_repeat property value."""
        return self.get_step_and_repeat().get_y_repeat()

    def set_y_repeat(self, value: int) -> Self:
        """Set the y_repeat property value."""
        return self.set_step_and_repeat(
            self.get_step_and_repeat().set_y_repeat(value),
        )

    def get_x_step(self) -> Offset:
        """Get x_step property value."""
        return self.get_step_and_repeat().get_x_step()

    def set_x_step(self, value: Offset) -> Self:
        """Set the x_repeat property value."""
        return self.set_step_and_repeat(
            self.get_step_and_repeat().set_x_step(value),
        )

    def get_y_step(self) -> Offset:
        """Get y_step property value."""
        return self.get_step_and_repeat().get_y_step()

    def set_y_step(self, value: Offset) -> Self:
        """Set the y_repeat property value."""
        return self.set_step_and_repeat(
            self.get_step_and_repeat().set_y_step(value),
        )

    current_position: Vector2D = Vector2D(x=Offset.NULL, y=Offset.NULL)
    """Current position of drawing head."""

    def get_current_position(self) -> Vector2D:
        """Get current_position property value."""
        return self.current_position

    def set_current_position(self, current_position: Vector2D) -> Self:
        """Set the current_position property value."""
        return self.model_copy(
            update={
                "current_position": current_position,
            },
        )

    current_aperture_id: Optional[ApertureID] = None
    """Reference to currently selected aperture."""

    def get_current_aperture_id(self) -> Optional[ApertureID]:
        """Get current_aperture property value."""
        return self.current_aperture_id

    def set_current_aperture_id(self, current_aperture: Optional[ApertureID]) -> Self:
        """Set the current_aperture property value."""
        return self.model_copy(
            update={
                "current_aperture_id": current_aperture,
            },
        )

    macros: State2MacroIndex = Field(default_factory=State2MacroIndex)
    """Collection of all macros defined until given point in code."""

    def get_macro(self, __key: str) -> ApertureMacro2:
        """Get macros property value."""
        return self.macros.get_macro(__key)

    def set_macro(self, __key: str, __value: ApertureMacro2) -> Self:
        """Set the macros property value."""
        return self.model_copy(
            update={
                "macros": self.macros.set_macro(__key, __value),
            },
        )

    def parse_coordinate(self, coordinate: Coordinate) -> Offset:
        """Parse a coordinate and convert it to an Offset.

        This method parses a given coordinate and converts it to an Offset object.
        It handles missing X, Y by substituting them with the current
        position and missing I, J by substituting them with NULL offset.

        Parameters
        ----------
        coordinate : Coordinate
            The coordinate to be parsed.

        Returns
        -------
        Offset
            The parsed coordinate converted to an Offset object.

        """
        if coordinate.coordinate_type == CoordinateType.MISSING_X:
            return self.current_position.x

        if coordinate.coordinate_type == CoordinateType.MISSING_Y:
            return self.current_position.y

        if coordinate.coordinate_type == CoordinateType.MISSING_I:
            return Offset.NULL

        if coordinate.coordinate_type == CoordinateType.MISSING_J:
            return Offset.NULL

        return Offset.new(
            self.get_coordinate_parser().parse(coordinate),
            unit=self.get_draw_units(),
        )
