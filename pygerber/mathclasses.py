# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from math import acos, sqrt, tau
from typing import SupportsIndex, Tuple


@dataclass
class Vector2D:
    x: float
    y: float

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other: SupportsIndex) -> Vector2D:
        return Vector2D(other[0] + self.x, other[1] + self.y)

    def __sub__(self, other: SupportsIndex) -> Vector2D:
        return Vector2D(self.x - other[0], self.y - other[1])

    def __mul__(self, other: float) -> Vector2D:
        return Vector2D(self.x * other, self.y * other)

    def __getitem__(self, index: int) -> float:
        return self.as_tuple()[index]

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    __len__ = length

    def dot(self, other: Vector2D) -> float:
        return self.x * other.x + self.y * other.y

    def normalize(self):
        length = len(self)
        return Vector2D(
            self.x / length,
            self.y / length,
        )


UNIT_VECTOR_X = Vector2D(1, 0)
UNIT_VECTOR_Y = Vector2D(0, 1)


def angle_from_zero(vector: Vector2D) -> float:
    raw_angle = acos(vector.dot(UNIT_VECTOR_X) / vector.length())
    if vector.y > 0:
        return raw_angle
    else:
        return tau - raw_angle


@dataclass
class BoundingBox:

    left: float
    upper: float
    right: float
    lower: float

    def __init__(self, x0: float, y0: float, x1: float, y1: float) -> None:
        """
        Coordinates are called x0, x1, y0, y1 on purpose - any of x's can be left.
        During assignment smaller one will be picked to be left, bigger one to be right.
        Same thing applies to y's. Order of coordinates doesn't mether as long
        as axes are preserved.
        """
        self.left = min(x0, x1)
        self.right = max(x0, x1)
        self.upper = max(y0, y1)
        self.lower = min(y0, y1)

    def as_tuple(self) -> Tuple[float]:
        """Tuple (left, upper, right, lower)"""
        return self.left, self.upper, self.right, self.lower

    def contains(self, other: BoundingBox) -> bool:
        return (
            self.left <= other.left
            and self.upper >= other.upper
            and self.right >= other.upper
            and self.lower <= other.lower
        )

    def padded(self, delta) -> None:
        return BoundingBox(
            self.left - delta,
            self.upper + delta,
            self.right + delta,
            self.lower - delta,
        )

    def height(self) -> float:
        return abs(self.upper - self.lower)

    def width(self) -> float:
        return abs(self.right - self.left)

    def transform(self, vector: Vector2D) -> BoundingBox:
        return BoundingBox(
            self.left + vector.x,
            self.upper + vector.y,
            self.right + vector.x,
            self.lower + vector.y,
        )

    def __add__(self, other):
        if isinstance(other, BoundingBox):
            return BoundingBox(
                min(self.left, other.left),
                max(self.upper, other.upper),
                max(self.right, other.right),
                min(self.lower, other.lower),
            )
        elif isinstance(other, Vector2D):
            return self.transform(other)
        else:
            raise TypeError(f"Type {type(other).__qualname__} addition not supported.")
