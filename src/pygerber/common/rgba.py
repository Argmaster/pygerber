"""RGBA colors are used for declaring visuals of rendering output.

This module contains RGBA class which can be used to provide such color.
"""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

import pydantic

from pygerber.common.frozen_general_model import FrozenGeneralModel

if TYPE_CHECKING:
    from typing_extensions import Self

ColorField = pydantic.Field(ge=0, le=255)
Color = int


HSV_Q0_MAX_ANGLE_DEGREES = 60
HSV_Q1_MAX_ANGLE_DEGREES = 120
HSV_Q2_MAX_ANGLE_DEGREES = 180
HSV_Q3_MAX_ANGLE_DEGREES = 240
HSV_Q4_MAX_ANGLE_DEGREES = 300
HSV_Q5_MAX_ANGLE_DEGREES = 360


class RGBA(FrozenGeneralModel):
    """Representation of RGBA color."""

    r: Color = ColorField
    g: Color = ColorField
    b: Color = ColorField
    a: Color = ColorField

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
            r=int(r, base=16),
            g=int(g, base=16),
            b=int(b, base=16),
            a=int(a, base=16),
        )

    @classmethod
    def from_rgba(cls, r: int, g: int, b: int, a: int = 0xFF) -> Self:
        """Build RGBA color object from reg, green, blue and alpha integer values.

        Parameters
        ----------
        r : int
            Red chanel value as integer from 0 to 255, inclusive.
        g : int
            Green chanel value as integer from 0 to 255, inclusive.
        b : int
            Blue chanel value as integer from 0 to 255, inclusive.
        a : int, optional
            Alpha chanel value as integer from 0 to 255, inclusive., by default 0xFF

        Returns
        -------
        Self
            Color built from r, g, b, a values.

        """
        return cls(r=r, g=g, b=b, a=a)

    @classmethod
    def from_hsv(
        cls,
        h: int,
        s: float,
        v: float,
        a: int = 255,
    ) -> Self:
        """Build RGBA color object from hue, saturation, value and alpha.

        For extended information refer to Wikipedia: https://en.wikipedia.org/wiki/HSL_and_HSV

        Parameters
        ----------
        h : int
            Hue of color, integer in range 0 to 360 inclusive.
        s : float
            Saturation of color, float in range 0.0 to 100.0 inclusive.
        v : float
            Value of color, float in range 0.0 to 100.0 inclusive.
        a : int
            Alpha of color, int in range 0 to 255 inclusive.

        Returns
        -------
        Self
            Color built from h, s, v, a values.

        """
        h %= 360
        s /= 100
        v /= 100

        c = v * s
        x = c * (1 - abs(((h / 60) % 2) - 1))
        m = v - c

        if 0 <= h < HSV_Q0_MAX_ANGLE_DEGREES:
            r_, g_, b_ = c, x, 0.0
        elif HSV_Q0_MAX_ANGLE_DEGREES <= h < HSV_Q1_MAX_ANGLE_DEGREES:
            r_, g_, b_ = x, c, 0.0
        elif HSV_Q1_MAX_ANGLE_DEGREES <= h < HSV_Q2_MAX_ANGLE_DEGREES:
            r_, g_, b_ = 0.0, c, x
        elif HSV_Q2_MAX_ANGLE_DEGREES <= h < HSV_Q3_MAX_ANGLE_DEGREES:
            r_, g_, b_ = 0.0, x, c
        elif HSV_Q3_MAX_ANGLE_DEGREES <= h < HSV_Q4_MAX_ANGLE_DEGREES:
            r_, g_, b_ = x, 0.0, c
        elif HSV_Q4_MAX_ANGLE_DEGREES <= h <= HSV_Q5_MAX_ANGLE_DEGREES:
            r_, g_, b_ = c, 0.0, x
        else:
            raise ValueError(h)

        return cls(
            r=round((r_ + m) * 255),
            g=round((g_ + m) * 255),
            b=round((b_ + m) * 255),
            a=a,
        )

    def as_rgba_int(self) -> tuple[int, int, int, int]:
        """Return RGBA color as tuple of integers in range 0 to 255 inclusive."""
        return self.r, self.g, self.b, self.a

    def as_rgb_int(self) -> tuple[int, int, int]:
        """Return RGB color as tuple of integers in range 0 to 255 inclusive."""
        return self.r, self.g, self.b

    def as_rgba_float(self) -> tuple[float, float, float, float]:
        """Return RGBA color as tuple of floats in range 0.0 to 1.0 inclusive."""
        return (
            float(Decimal(self.r) / Decimal(255)),
            float(Decimal(self.g) / Decimal(255)),
            float(Decimal(self.b) / Decimal(255)),
            float(Decimal(self.a) / Decimal(255)),
        )

    def to_hex(self) -> str:
        """Return color as hexadecimal string.

        Eg. `#FF0000FF` for red color.
        """
        r = f"{self.r:0{2}x}"
        g = f"{self.g:0{2}x}"
        b = f"{self.b:0{2}x}"
        a = f"{self.a:0{2}x}"
        return f"#{r}{g}{b}{a}"
