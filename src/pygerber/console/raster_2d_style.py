"""Tool for converting style string to ColorScheme objects."""

from __future__ import annotations

from typing import Optional

from pygerber.backend.rasterized_2d.color_scheme import ColorScheme
from pygerber.common.rgba import RGBA

CUSTOM_STYLE_OPTION = "custom"

STYLE_TO_COLOR_SCHEME = {
    "silk": ColorScheme.SILK,
    "silk_alpha": ColorScheme.SILK_ALPHA,
    "copper": ColorScheme.COPPER,
    "copper_alpha": ColorScheme.COPPER_ALPHA,
    "paste_mask": ColorScheme.PASTE_MASK,
    "paste_mask_alpha": ColorScheme.PASTE_MASK_ALPHA,
    "solder_mask": ColorScheme.SOLDER_MASK,
    "solder_mask_alpha": ColorScheme.SOLDER_MASK_ALPHA,
    "default_grayscale": ColorScheme.DEFAULT_GRAYSCALE,
    "debug_1": ColorScheme.DEBUG_1,
    CUSTOM_STYLE_OPTION: None,
}
"""Map of known color styles to ColorScheme objects."""


def get_color_scheme_from_style(
    style: str,
    custom: Optional[str] = None,
) -> ColorScheme:
    """Convert style string to ColorScheme object.

    Accepted values for style are any key from STYLE_TO_COLOR_SCHEME. When style is
    'custom' then parameter custom must also be provided.
    Custom color should be a single string consisting of 5 or 7 valid hexadecimal colors
    separated with commas. Any color which can be parsed by RGBA type is accepted.
    Colors are assigned in order:

    - background_color
    - clear_color
    - solid_color
    - clear_region_color
    - solid_region_color
    - debug_1_color (optional, by default #ABABAB)
    - debug_2_color (optional, by default #7D7D7D)

    eg. `"000000,000000,FFFFFF,000000,FFFFFF"`
    """
    if style == CUSTOM_STYLE_OPTION:
        if custom is None:
            msg = (
                f"When style is {CUSTOM_STYLE_OPTION!r} custom have to be a valid "
                "custom scheme."
            )
            raise TypeError(msg)
        return _construct_custom_scheme(custom)

    color_scheme = STYLE_TO_COLOR_SCHEME[style]
    if color_scheme is None:
        # Can't happen - option 'custom' is picked by if above.
        raise TypeError

    return color_scheme


def _construct_custom_scheme(custom: str) -> ColorScheme:
    (
        background_color,
        clear_color,
        solid_color,
        clear_region_color,
        solid_region_color,
        *debug_colors,
    ) = custom.strip().split(",")

    return ColorScheme(
        background_color=RGBA.from_hex(background_color),
        clear_color=RGBA.from_hex(clear_color),
        solid_color=RGBA.from_hex(solid_color),
        clear_region_color=RGBA.from_hex(clear_region_color),
        solid_region_color=RGBA.from_hex(solid_region_color),
        debug_1_color=(
            RGBA.from_hex(debug_colors[0])
            if len(debug_colors) > 0
            else RGBA.from_hex("#ababab")
        ),
        debug_2_color=(
            RGBA.from_hex(debug_colors[0])
            if len(debug_colors) > 0
            else RGBA.from_hex("#7d7d7d")
        ),
    )
