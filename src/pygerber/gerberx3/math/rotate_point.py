"""Tool for rotating point around center."""

from __future__ import annotations

from math import cos, sin
from typing import TYPE_CHECKING

from pygerber.gerberx3.math.vector_2d import Vector2D

if TYPE_CHECKING:
    from decimal import Decimal


def rotate_point(center: Vector2D, angle: Decimal | float, point: Vector2D) -> Vector2D:
    """Rotate point around center by given angle."""
    s = sin(angle)
    c = cos(angle)

    # Translate point back to origin
    x, y = point.x, point.y
    x -= center.x
    y -= center.y

    # Rotate point
    x_new = x * c - y * s
    y_new = x * s + y * c

    # Translate point back
    x = x_new + center.x
    y = y_new + center.y

    return Vector2D(x=x, y=y)
