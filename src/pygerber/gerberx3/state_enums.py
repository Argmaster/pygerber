"""All state-defining enumerations."""
from __future__ import annotations

from enum import Enum


class DrawMode(Enum):
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


class Polarity(Enum):
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


class Mirroring(Enum):
    """Aperture mirroring."""

    NoMirroring = "N"
    XY = "XY"
    X = "X"
    Y = "Y"


class Unit(Enum):
    """Aperture unit."""

    Millimeters = "MM"
    Inches = "IN"
