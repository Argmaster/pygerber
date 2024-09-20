"""RGBA colors are used for declaring visuals of rendering output.

This module contains RGBA class which can be used to provide such color.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import pydantic

from pygerber.vm.types.model import ModelType

if TYPE_CHECKING:
    from typing_extensions import Self

ChannelField = pydantic.Field(ge=0, le=255)
ChannelType = int


HSV_Q0_MAX_ANGLE_DEGREES = 60
HSV_Q1_MAX_ANGLE_DEGREES = 120
HSV_Q2_MAX_ANGLE_DEGREES = 180
HSV_Q3_MAX_ANGLE_DEGREES = 240
HSV_Q4_MAX_ANGLE_DEGREES = 300
HSV_Q5_MAX_ANGLE_DEGREES = 360


class Color(ModelType):
    """Color class represents a RGBA color.

    Channels are represented as integers in range 0 to 255.
    """

    red: ChannelType = ChannelField
    """Red channel value."""

    green: ChannelType = ChannelField
    """Green channel value."""

    blue: ChannelType = ChannelField
    """Blue channel value."""

    alpha: ChannelType = ChannelField
    """Alpha channel value."""

    @classmethod
    def from_hex(cls, string: str) -> Self:
        """Build RGBA color object from hexadecimal string.

        Parameters
        ----------
        string : str
            String containing color value. Accepted formats are `RRGGBBAA` and `RRGGBB`.
            For latter, alpha value is assumed to be 0xFF. Formats are case insensitive.
            `#` symbol prefix for hex string is accepted.

        Returns
        -------
        RGBA
            Color built from hexadecimal values.

        """
        if string[0] == "#":
            string = string[1:]

        r, g, b, a = string[:2], string[2:4], string[4:6], string[6:]
        if len(a) == 0:
            a = "FF"

        return cls(
            red=int(r, base=16),
            green=int(g, base=16),
            blue=int(b, base=16),
            alpha=int(a, base=16),
        )

    @classmethod
    def from_rgba(cls, red: int, green: int, blue: int, alpha: int = 0xFF) -> Self:
        """Build RGBA color object from reg, green, blue and alpha integer values.

        Parameters
        ----------
        red : int
            Red chanel value as integer from 0 to 255, inclusive.
        green : int
            Green chanel value as integer from 0 to 255, inclusive.
        blue : int
            Blue chanel value as integer from 0 to 255, inclusive.
        alpha : int, optional
            Alpha chanel value as integer from 0 to 255, inclusive., by default 0xFF

        Returns
        -------
        Self
            Color built from r, g, b, a values.

        """
        return cls(red=red, green=green, blue=blue, alpha=alpha)

    @classmethod
    def from_hsv(
        cls,
        hue: int,
        saturation: float,
        value: float,
        alpha: int = 255,
    ) -> Self:
        """Build RGBA color object from hue, saturation, value and alpha.

        For extended information refer to Wikipedia: https://en.wikipedia.org/wiki/HSL_and_HSV

        Parameters
        ----------
        hue : int
            Hue of color, integer in range 0 to 360 inclusive.
        saturation : float
            Saturation of color, float in range 0.0 to 100.0 inclusive.
        value : float
            Value of color, float in range 0.0 to 100.0 inclusive.
        alpha : int
            Alpha of color, int in range 0 to 255 inclusive.

        Returns
        -------
        Self
            Color built from h, s, v, a values.

        """
        hue %= 360
        saturation /= 100
        value /= 100

        c = value * saturation
        x = c * (1 - abs(((hue / 60) % 2) - 1))
        m = value - c

        if 0 <= hue < HSV_Q0_MAX_ANGLE_DEGREES:
            r_, g_, b_ = c, x, 0.0
        elif HSV_Q0_MAX_ANGLE_DEGREES <= hue < HSV_Q1_MAX_ANGLE_DEGREES:
            r_, g_, b_ = x, c, 0.0
        elif HSV_Q1_MAX_ANGLE_DEGREES <= hue < HSV_Q2_MAX_ANGLE_DEGREES:
            r_, g_, b_ = 0.0, c, x
        elif HSV_Q2_MAX_ANGLE_DEGREES <= hue < HSV_Q3_MAX_ANGLE_DEGREES:
            r_, g_, b_ = 0.0, x, c
        elif HSV_Q3_MAX_ANGLE_DEGREES <= hue < HSV_Q4_MAX_ANGLE_DEGREES:
            r_, g_, b_ = x, 0.0, c
        elif HSV_Q4_MAX_ANGLE_DEGREES <= hue <= HSV_Q5_MAX_ANGLE_DEGREES:
            r_, g_, b_ = c, 0.0, x
        else:
            raise ValueError(hue)

        return cls(
            red=round((r_ + m) * 255),
            green=round((g_ + m) * 255),
            blue=round((b_ + m) * 255),
            alpha=alpha,
        )

    def as_rgba_int(self) -> tuple[int, int, int, int]:
        """Return RGBA color as tuple of integers in range 0 to 255 inclusive."""
        return self.red, self.green, self.blue, self.alpha

    def as_rgb_int(self) -> tuple[int, int, int]:
        """Return RGB color as tuple of integers in range 0 to 255 inclusive."""
        return self.red, self.green, self.blue

    def as_rgba_float(self) -> tuple[float, float, float, float]:
        """Return RGBA color as tuple of floats in range 0.0 to 1.0 inclusive."""
        return (
            float(Decimal(self.red) / Decimal(255)),
            float(Decimal(self.green) / Decimal(255)),
            float(Decimal(self.blue) / Decimal(255)),
            float(Decimal(self.alpha) / Decimal(255)),
        )

    def to_hex(self) -> str:
        """Return color as hexadecimal string.

        Eg. `#FF0000FF` for red color.
        """
        r = f"{self.red:0{2}x}"
        g = f"{self.green:0{2}x}"
        b = f"{self.blue:0{2}x}"
        a = f"{self.alpha:0{2}x}"
        return f"#{r}{g}{b}{a}"
