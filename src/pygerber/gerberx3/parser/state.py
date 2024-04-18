"""Global drawing state containing configuration which can be altered by tokens."""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Optional

from pydantic import Field

from pygerber.backend.abstract.aperture_handle import PublicApertureHandle
from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.offset import Offset
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser.errors import (
    ApertureNotSelectedError,
    CoordinateFormatNotSetError,
    UnitNotSetError,
)
from pygerber.gerberx3.state_enums import DrawMode, Mirroring, Polarity, Unit
from pygerber.gerberx3.tokenizer.tokens.coordinate import Coordinate, CoordinateType
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    CoordinateParser,
)
from pygerber.gerberx3.tokenizer.tokens.macro.am_macro import MacroDefinition


class State(FrozenGeneralModel):
    """GerberX3 interpreter state."""

    current_position: Vector2D = Vector2D(x=Offset.NULL, y=Offset.NULL)

    # MO | Mode | Sets the unit to mm or inch                           | 4.2.1
    draw_units: Optional[Unit] = None
    # FS | Format specification | Sets the coordinate format,           | 4.2.2
    #    |                      | e.g. the number of decimals
    coordinate_parser: Optional[CoordinateParser] = None
    # Dnn | (nn≥10) | Sets the current aperture to D code nn.           | 4.6
    current_aperture: Optional[PublicApertureHandle] = None
    # G01 | | Sets linear/circular mode to linear.                      | 4.7.1
    # G02 | | Sets linear/circular mode to clockwise circular           | 4.7.2
    # G03 | | Sets linear/circular mode to counterclockwise circular    | 4.7.3
    draw_mode: DrawMode = DrawMode.Linear
    # LP  | | Load polarity | Loads the polarity object transformation  | 4.9.2
    #                       parameter.
    polarity: Polarity = Polarity.Dark
    # LM  | | Load mirroring | Loads the mirror object transformation   | 4.9.3
    #                         parameter.
    mirroring: Mirroring = Mirroring.NoMirroring
    # LR  | Load rotation |  Loads the rotation object transformation   | 4.9.4
    #                       parameter.
    rotation: Decimal = Decimal("0.0")

    region_boundary_points: List[Vector2D] = Field(default_factory=list)
    """Points defining the shape of the region."""

    # LS  | Load scaling |   Loads the scale object transformation      | 4.9.5
    #                       parameter
    scaling: Decimal = Decimal("1.0")
    # G36 | |   Starts a region statement which creates a region by     | 4.10
    #     | |   defining its contours.
    # G37 | |   Ends the region statement.                              | 4.10
    is_region: bool = False
    # AB  | |   Aperture blockOpens a block aperture statement and      | 4.11
    #     | |   assigns its aperture number or closes a block aperture  |
    #     | |   statement.                                              |
    is_aperture_block: bool = False
    # SR  | |   Step and repeatOpen or closes a step and repeat         | 4.11
    #     | |   statement.                                              |
    is_step_and_repeat: bool = False
    # TF  | |   Attribute on fileSet a file attribute.                  | 5.3
    # TD  | |   Attribute deleteDelete one or all attributes in the     | 5.5
    #     | |   dictionary.                                             |
    file_attributes: Dict[str, str] = Field(default_factory=dict)
    # G75 | |   Sets multi quadrant mode
    # G74 | |   Sets single quadrant mode
    is_multi_quadrant: bool = False

    is_output_image_negation_required: bool = False
    """In Gerber specification deprecated IP command is mentioned.
    It can set image polarity to either positive, the usual one, or to negative.
    Under negative image polarity, image generation is different. Its purpose is to
    create a negative image, clear areas in a dark background. The entire image plane
    in the background is initially dark instead of clear. The effect of dark and clear
    polarity is toggled. The entire image is simply reversed, dark becomes white and
    vice versa.
    This effect can be achieved by simply inverting colors of output image.
    """

    apertures: Dict[ApertureID, PublicApertureHandle] = Field(default_factory=dict)
    """Collection of all apertures defined until given point in code."""

    macros: Dict[str, MacroDefinition] = Field(default_factory=dict)
    """Collection of all macros defined until given point in code."""

    def get_units(self) -> Unit:
        """Get drawing unit or raise UnitNotSetError."""
        if self.draw_units is None:
            raise UnitNotSetError
        return self.draw_units

    def get_coordinate_parser(self) -> CoordinateParser:
        """Get coordinate parser or raise CoordinateFormatNotSetError."""
        if self.coordinate_parser is None:
            raise CoordinateFormatNotSetError
        return self.coordinate_parser

    def get_current_aperture(self) -> PublicApertureHandle:
        """Get current aperture or raise ApertureNotSelectedError."""
        if self.current_aperture is None:
            raise ApertureNotSelectedError
        return self.current_aperture

    def parse_coordinate(self, coordinate: Coordinate) -> Offset:
        """Parse, include substitution with current and conversion to Offset."""
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
            unit=self.get_units(),
        )
