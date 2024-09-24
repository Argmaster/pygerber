"""`style` module contains `Style` class which represents colors of rendered image."""

from __future__ import annotations

from typing import ClassVar

from pygerber.common.namespace import Namespace
from pygerber.vm.types.color import Color
from pygerber.vm.types.model import ModelType


class Style(ModelType):
    """Style class represents colors which should be used for coloring rendered image
    layer.
    """

    foreground: Color
    background: Color

    class presets(Namespace):  # noqa: N801
        """`Style.presets` contains predefined styles for convenience."""

        SILK: ClassVar[Style]
        """Default color of silk layer.

        This schema provided non-transparent background, which results in images which
        can not be used for stacking on top of other layers, as they would completely
        obscure them."""

        SILK_ALPHA: ClassVar[Style]
        """Default color of silk layer with alpha channel.

        This schema provides transparent background. Images using this schema can be
        stacked on top of each other without obscuring layers below."""

        COPPER: ClassVar[Style]
        """Default color of copper layer.

        This schema provided non-transparent background, which results in images which
        can not be used for stacking on top of other layers, as they would completely
        obscure them."""

        COPPER_ALPHA: ClassVar[Style]
        """Default color of copper layer with alpha channel.

        This schema provides transparent background. Images using this schema can be
        stacked on top of each other without obscuring layers below."""

        PASTE_MASK: ClassVar[Style]
        """Default color of paste mask layer.

        This schema provided non-transparent background, which results in images which
        can not be used for stacking on top of other layers, as they would completely
        obscure them."""

        PASTE_MASK_ALPHA: ClassVar[Style]
        """Default color of paste mask layer with alpha channel.

        This schema provides transparent background. Images using this schema can be
        stacked on top of each other without obscuring layers below."""

        SOLDER_MASK: ClassVar[Style]
        """Default color of solder mask layer.

        This schema provided non-transparent background, which results in images which
        can not be used for stacking on top of other layers, as they would completely
        obscure them."""

        SOLDER_MASK_ALPHA: ClassVar[Style]
        """Default color of solder mask layer with alpha channel.

        This schema provides transparent background. Images using this schema can be
        stacked on top of each other without obscuring layers below."""

        DEFAULT_GRAYSCALE: ClassVar[Style]
        """Default color scheme for files which were not assigned other color scheme."""

        DEBUG_1: ClassVar[Style]
        """Debug color scheme."""

        DEBUG_1_ALPHA: ClassVar[Style]
        """Debug color scheme with alpha channel."""

        BLACK_WHITE: ClassVar[Style]
        """Black and white color scheme."""

        BLACK_WHITE_ALPHA: ClassVar[Style]
        """Black and white color scheme with alpha channel."""


Style.presets.SILK = Style(
    background=Color.from_hex("#000000"),
    foreground=Color.from_hex("#FFFFFF"),
)
Style.presets.SILK_ALPHA = Style(
    background=Color.from_hex("#00000000"),
    foreground=Color.from_hex("#FFFFFFFF"),
)

Style.presets.COPPER = Style(
    background=Color.from_rgba(0, 0, 0, 255),
    foreground=Color.from_rgba(40, 143, 40, 255),
)
Style.presets.COPPER_ALPHA = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(40, 143, 40, 255),
)

Style.presets.PASTE_MASK = Style(
    background=Color.from_rgba(0, 0, 0, 255),
    foreground=Color.from_rgba(117, 117, 117, 255),
)
Style.presets.PASTE_MASK_ALPHA = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(117, 117, 117, 255),
)

Style.presets.SOLDER_MASK = Style(
    background=Color.from_rgba(0, 0, 0, 255),
    foreground=Color.from_rgba(117, 117, 117, 255),
)
Style.presets.SOLDER_MASK_ALPHA = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(153, 153, 153, 255),
)

Style.presets.DEFAULT_GRAYSCALE = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(255, 255, 255, 255),
)

Style.presets.DEBUG_1 = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(19, 61, 145, 255),
)
Style.presets.DEBUG_1_ALPHA = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(19, 61, 145, 255),
)

Style.presets.BLACK_WHITE = Style(
    background=Color.from_rgba(0, 0, 0, 255),
    foreground=Color.from_rgba(255, 255, 255, 255),
)
Style.presets.BLACK_WHITE_ALPHA = Style(
    background=Color.from_rgba(0, 0, 0, 0),
    foreground=Color.from_rgba(255, 255, 255, 255),
)
