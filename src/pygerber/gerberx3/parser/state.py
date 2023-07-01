from __future__ import annotations

from dataclasses import dataclass


class State:
    """GerberX3 interpreter state."""

    def __init__(self) -> None:
        """Initialize interpreter state."""
        # MO | Mode | Sets the unit to mm or inch                           | 4.2.1
        self.draw_units = None
        # FS | Format specification | Sets the coordinate format,           | 4.2.2
        #    |                      | e.g. the number of decimals
        self.coordinate_format = None
        # Dnn | (nn≥10) | Sets the current aperture to D code nn.           | 4.6
        self.current_aperture = None
        # G01 | | Sets linear/circular mode to linear.                      | 4.7.1
        # G02 | | Sets linear/circular mode to clockwise circular           | 4.7.2
        # G03 | | Sets linear/circular mode to counterclockwise circular    | 4.7.3
        self.draw_mode = None
        # LP  | | Load polarity | Loads the polarity object transformation  | 4.9.2
        #                       parameter.
        self.polarity = None
        # LM  | | Load mirroring | Loads the mirror object transformation   | 4.9.3
        #                         parameter.
        self.mirroring = None
        # LR  | Load rotation |  Loads the rotation object transformation   | 4.9.4
        #                       parameter.
        self.rotation = None
        # LS  | Load scaling |   Loads the scale object transformation      | 4.9.5
        #                       parameter
        self.scaling = None
        # G36 | |   Starts a region statement which creates a region by     | 4.10
        #     | |   defining its contours.
        # G37 | |   Ends the region statement.                              | 4.10
        self.is_region = None
        # AB  | |   Aperture blockOpens a block aperture statement and      | 4.11
        #     | |   assigns its aperture number or closes a block aperture  |
        #     | |   statement.                                              |
        self.is_aperture_block = None
        # SR  | |   Step and repeatOpen or closes a step and repeat         | 4.11
        #     | |   statement.                                              |
        self.is_step_and_repeat = None
        # TF  | |   Attribute on fileSet a file attribute.                  | 5.3
        # TD  | |   Attribute deleteDelete one or all attributes in the     | 5.5
        #     | |   dictionary.                                             |
        self.file_attributes: dict[str, str] = {}
        self.apertures: dict[str, ApertureConfig]


@dataclass
class ApertureConfig:
    pass
