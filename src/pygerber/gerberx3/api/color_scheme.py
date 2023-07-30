"""ColorScheme class - utility for describing color schemes."""

from __future__ import annotations

from typing import ClassVar

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.rgba import RGBA


class ColorScheme(FrozenGeneralModel):
    """Description of colors which should be used for rendering."""

    SILK: ClassVar[ColorScheme]
    """Default color of silk layer."""

    SILK_ALPHA: ClassVar[ColorScheme]
    """Default color of silk layer with alpha channel."""

    COPPER: ClassVar[ColorScheme]
    """Default color of copper layer."""

    COPPER_ALPHA: ClassVar[ColorScheme]
    """Default color of copper layer with alpha channel."""

    PASTE_MASK: ClassVar[ColorScheme]
    """Default color of paste mask layer."""

    PASTE_MASK_ALPHA: ClassVar[ColorScheme]
    """Default color of paste mask layer with alpha channel."""

    SOLDER_MASK: ClassVar[ColorScheme]
    """Default color of solder mask layer."""

    SOLDER_MASK_ALPHA: ClassVar[ColorScheme]
    """Default color of solder mask layer with alpha channel."""

    background_color: RGBA
    """Color used as empty image background."""

    clear_color: RGBA
    """Color used for clear draws."""

    solid_color: RGBA
    """Color used for solid draws."""

    clear_region_color: RGBA
    """Color used for clear region draws."""

    solid_region_color: RGBA
    """Color used for solid region draws."""

    debug_1_color: RGBA = RGBA.from_hex("#ababab")
    """Color used for debug elements."""

    debug_2_color: RGBA = RGBA.from_hex("#7d7d7d")
    """Color used for debug elements."""


ColorScheme.SILK = ColorScheme(
    background_color=RGBA.from_hex("#000000"),
    clear_color=RGBA.from_hex("#000000"),
    solid_color=RGBA.from_hex("#FFFFFF"),
    clear_region_color=RGBA.from_hex("#000000"),
    solid_region_color=RGBA.from_hex("#FFFFFF"),
)
ColorScheme.SILK_ALPHA = ColorScheme(
    background_color=RGBA.from_hex("#00000000"),
    clear_color=RGBA.from_hex("#00000000"),
    solid_color=RGBA.from_hex("#FFFFFFFF"),
    clear_region_color=RGBA.from_hex("#00000000"),
    solid_region_color=RGBA.from_hex("#FFFFFFFF"),
)

ColorScheme.COPPER = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 255),
    clear_color=RGBA.from_rgba(60, 181, 60, 255),
    solid_color=RGBA.from_rgba(40, 143, 40, 255),
    clear_region_color=RGBA.from_rgba(60, 181, 60, 255),
    solid_region_color=RGBA.from_rgba(40, 143, 40, 255),
)
ColorScheme.COPPER_ALPHA = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(60, 181, 60, 255),
    solid_color=RGBA.from_rgba(40, 143, 40, 255),
    clear_region_color=RGBA.from_rgba(60, 181, 60, 255),
    solid_region_color=RGBA.from_rgba(40, 143, 40, 255),
)

ColorScheme.PASTE_MASK = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 255),
    clear_color=RGBA.from_rgba(0, 0, 0, 255),
    solid_color=RGBA.from_rgba(117, 117, 117, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 255),
    solid_region_color=RGBA.from_rgba(117, 117, 117, 255),
)
ColorScheme.PASTE_MASK_ALPHA = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_color=RGBA.from_rgba(117, 117, 117, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_region_color=RGBA.from_rgba(117, 117, 117, 255),
)

ColorScheme.SOLDER_MASK = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 255),
    clear_color=RGBA.from_rgba(0, 0, 0, 255),
    solid_color=RGBA.from_rgba(117, 117, 117, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 255),
    solid_region_color=RGBA.from_rgba(117, 117, 117, 255),
)
ColorScheme.SOLDER_MASK_ALPHA = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_color=RGBA.from_rgba(153, 153, 153, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_region_color=RGBA.from_rgba(153, 153, 153, 255),
)
