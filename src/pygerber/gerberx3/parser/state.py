"""Global drawing state containing configuration which can be altered by tokens."""
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional, Tuple

from pydantic import BaseModel, ConfigDict

from pygerber.backend.abstract.aperture_handle import ApertureHandle
from pygerber.gerberx3.tokenizer.tokens.dnn_select_aperture import ApertureID
from pygerber.gerberx3.tokenizer.tokens.fs_coordinate_format import (
    CoordinateParser,
)
from pygerber.gerberx3.tokenizer.tokens.g0n_set_draw_mode import DrawMode
from pygerber.gerberx3.tokenizer.tokens.lm_load_mirroring import Mirroring
from pygerber.gerberx3.tokenizer.tokens.lp_load_polarity import Polarity
from pygerber.gerberx3.tokenizer.tokens.mo_unit_mode import Unit


class State(BaseModel):
    """GerberX3 interpreter state."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    current_position: Tuple[Decimal, Decimal] = (Decimal(0.0), Decimal(0.0))

    # MO | Mode | Sets the unit to mm or inch                           | 4.2.1
    draw_units: Optional[Unit] = None
    # FS | Format specification | Sets the coordinate format,           | 4.2.2
    #    |                      | e.g. the number of decimals
    coordinate_parser: Optional[CoordinateParser] = None
    # Dnn | (nn≥10) | Sets the current aperture to D code nn.           | 4.6
    current_aperture: Optional[ApertureID] = None
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
    rotation: float = 0.0
    # LS  | Load scaling |   Loads the scale object transformation      | 4.9.5
    #                       parameter
    scaling: float = 1.0
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
    file_attributes: Dict[str, str] = {}

    apertures: Dict[ApertureID, ApertureHandle] = {}
