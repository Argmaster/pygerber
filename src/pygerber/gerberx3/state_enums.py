"""All state-defining enumerations."""
from __future__ import annotations

from enum import Enum


class EnumFormatValue(Enum):
    """Enum subclass which when stringified shows its value."""

    def __str__(self) -> str:
        return str(self.value)


class DrawMode(EnumFormatValue):
    """Drawing mode."""

    Linear = "G01"
    """In linear plot mode a D01 operation generates a linear segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates.Outside a region statement the segment is stroked with the
    current aperture to create a draw graphical object. In a region statement the
    segment is added to the contour under construction."""

    ClockwiseCircular = "G02"
    """In circular plot mode a D01 operation generates an arc segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates. Outside a region statement the segment is stroked with the
    current aperture to create an arc graphical object. In a region statement the
    segment is added to the contour under construction. For compatibility with older
    versions of the Gerber format, a G75* must be issued before the first D01 in
    circular mode."""

    CounterclockwiseCircular = "G03"
    """In circular plot mode a D01 operation generates an arc segment, from the current
    point to the (X, Y) coordinates in the command. The current point is then set to the
    (X, Y) coordinates. Outside a region statement the segment is stroked with the
    current aperture to create an arc graphical object. In a region statement the
    segment is added to the contour under construction. For compatibility with older
    versions of the Gerber format, a G75* must be issued before the first D01 in
    circular mode."""


class Polarity(EnumFormatValue):
    """Aperture polarity."""

    Clear = "C"
    Dark = "D"
    DEBUG = "DBG"
    DEBUG2 = "DBG2"

    def invert(self) -> Polarity:
        """Return opposite polarity."""
        if self == Polarity.Clear:
            return Polarity.Dark

        return Polarity.Clear

    def get_2d_rasterized_color(self) -> int:
        """Get color for "1" mode image."""
        return _2d_rasterized_color_map[self]


_2d_rasterized_color_map = {
    Polarity.Dark: 255,
    Polarity.Clear: 0,
    Polarity.DEBUG: 127,
    Polarity.DEBUG2: 75,
}


class Mirroring(EnumFormatValue):
    """Aperture mirroring."""

    NoMirroring = "N"
    XY = "XY"
    X = "X"
    Y = "Y"


class Unit(EnumFormatValue):
    """Aperture unit."""

    Millimeters = "MM"
    Inches = "IN"


class ImagePolarityEnum(EnumFormatValue):
    """Image polarity.

    ### Image Polarity (IP)

    Note: The IP command is deprecated.

    The `IP` command is responsible for setting the polarity for the entire image. It is
    designed to be used only once, preferably at the very beginning of the file.

    #### 7.1.3.1 Positive Image Polarity
    Under the positive image polarity:
    - The image is generated in accordance with the specifications provided elsewhere in
        this document.
    - It's worth noting that, by default, image generation has always assumed a positive
        image polarity.

    #### 7.1.3.2 Negative Image Polarity
    When the negative image polarity is in use:
    - The intent is to produce an image that portrays clear areas against a dark
        backdrop.
    - The initial state of the entire image plane is dark, as opposed to being clear.
    - The polarity effects between dark and clear regions are interchanged. Essentially,
        what was dark becomes white and vice-versa.
    - For negative image polarity, the very first graphics object that gets produced
        must possess a dark polarity. As a result, it takes on the role of clearing the
        dark backdrop.
    """

    POSITIVE = "POS"
    NEGATIVE = "NEG"
