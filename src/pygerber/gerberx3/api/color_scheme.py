"""ColorScheme class - utility for describing color schemes."""

from __future__ import annotations

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.rgba import RGBA


class ColorScheme(FrozenGeneralModel):
    """Description of colors which should be used for rendering."""

    void_color: RGBA = RGBA.from_hex("#000000")
    solid_color: RGBA = RGBA.from_hex("#FFFFFF")
    region_color: RGBA = RGBA.from_hex("#FFFFFF")
    debug_1_color: RGBA = RGBA.from_hex("#ababab")
    debug_2_color: RGBA = RGBA.from_hex("#7d7d7d")
