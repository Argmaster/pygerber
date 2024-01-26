"""ColorScheme class - utility for describing color schemes."""

from __future__ import annotations

from typing import ClassVar

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.rgba import RGBA
from pygerber.gerberx3.state_enums import Polarity


class ColorScheme(FrozenGeneralModel):
    r"""Set of colors which should be used for rendering.

    ColorScheme class contains set of colors which should be used for different parts
    of rendered image. At the same time it also works as a container for predefined
    color schemes commonly used for parts of PCB.

    !!! info "Predefined colors"

        All predefined colors have two variants - normal one and one with "\*_ALPHA"
        suffix. Those without suffix have solid background and are not intended for
        constructing multi-layer images out of them ie. they are not suitable for
        rendering a project consisting of separate copper, silk, pase mask and composing
        them into single image. For cases when rendered images are intended for stacking
        "\*_ALPHA" schemes should be used, as background and transparent parts of image
        will be truly transparent.

    """

    SILK: ClassVar[ColorScheme]
    """Default color of silk layer.

    This schema provided non-transparent background, which results in images which
    can not be used for stacking on top of other layers, as they would completely
    obscure them."""

    SILK_ALPHA: ClassVar[ColorScheme]
    """Default color of silk layer with alpha channel.

    This schema provides transparent background. Images using this schema can be
    stacked on top of each other without obscuring layers below."""

    COPPER: ClassVar[ColorScheme]
    """Default color of copper layer.

    This schema provided non-transparent background, which results in images which
    can not be used for stacking on top of other layers, as they would completely
    obscure them."""

    COPPER_ALPHA: ClassVar[ColorScheme]
    """Default color of copper layer with alpha channel.

    This schema provides transparent background. Images using this schema can be
    stacked on top of each other without obscuring layers below."""

    PASTE_MASK: ClassVar[ColorScheme]
    """Default color of paste mask layer.

    This schema provided non-transparent background, which results in images which
    can not be used for stacking on top of other layers, as they would completely
    obscure them."""

    PASTE_MASK_ALPHA: ClassVar[ColorScheme]
    """Default color of paste mask layer with alpha channel.

    This schema provides transparent background. Images using this schema can be
    stacked on top of each other without obscuring layers below."""

    SOLDER_MASK: ClassVar[ColorScheme]
    """Default color of solder mask layer.

    This schema provided non-transparent background, which results in images which
    can not be used for stacking on top of other layers, as they would completely
    obscure them."""

    SOLDER_MASK_ALPHA: ClassVar[ColorScheme]
    """Default color of solder mask layer with alpha channel.

    This schema provides transparent background. Images using this schema can be
    stacked on top of each other without obscuring layers below."""

    DEFAULT_GRAYSCALE: ClassVar[ColorScheme]
    """Default color scheme for files which were not assigned other color scheme."""

    DEBUG_1: ClassVar[ColorScheme]
    """Debug color scheme."""

    DEBUG_1_ALPHA: ClassVar[ColorScheme]
    """Debug color scheme with alpha channel."""

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

    def get_grayscale_to_rgba_color_map(self) -> dict[int, tuple[int, int, int, int]]:
        """Return grayscale to RGBA color map."""
        return {
            Polarity.Dark.get_2d_rasterized_color(): self.solid_color.as_rgba_int(),
            Polarity.Clear.get_2d_rasterized_color(): self.clear_color.as_rgba_int(),
            Polarity.DarkRegion.get_2d_rasterized_color(): self.solid_region_color.as_rgba_int(),  # noqa: E501
            Polarity.ClearRegion.get_2d_rasterized_color(): self.clear_region_color.as_rgba_int(),  # noqa: E501
            Polarity.Background.get_2d_rasterized_color(): self.background_color.as_rgba_int(),  # noqa: E501
            Polarity.DEBUG.get_2d_rasterized_color(): self.debug_1_color.as_rgba_int(),
            Polarity.DEBUG2.get_2d_rasterized_color(): self.debug_2_color.as_rgba_int(),
        }


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

ColorScheme.DEFAULT_GRAYSCALE = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_color=RGBA.from_rgba(255, 255, 255, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_region_color=RGBA.from_rgba(255, 255, 255, 255),
    debug_1_color=RGBA.from_hex("#ababab"),
    debug_2_color=RGBA.from_hex("#7d7d7d"),
)

ColorScheme.DEBUG_1 = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(187, 8, 65, 255),
    solid_color=RGBA.from_rgba(19, 61, 145, 255),
    clear_region_color=RGBA.from_rgba(94, 52, 20, 255),
    solid_region_color=RGBA.from_rgba(21, 92, 130, 255),
    debug_1_color=RGBA.from_hex("#ababab"),
    debug_2_color=RGBA.from_hex("#7d7d7d"),
)
ColorScheme.DEBUG_1_ALPHA = ColorScheme(
    background_color=RGBA.from_rgba(0, 0, 0, 0),
    clear_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_color=RGBA.from_rgba(19, 61, 145, 255),
    clear_region_color=RGBA.from_rgba(0, 0, 0, 0),
    solid_region_color=RGBA.from_rgba(21, 92, 130, 255),
    debug_1_color=RGBA.from_hex("#ababab"),
    debug_2_color=RGBA.from_hex("#7d7d7d"),
)
