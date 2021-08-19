# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import SupportsIndex, Tuple


@dataclass
class Vector2D:
    x: float
    y: float

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other: SupportsIndex) -> Vector2D:
        return Vector2D(other[0] + self.x, other[1] + self.y)

    def __getitem__(self, index: int) -> float:
        return self.as_tuple()[index]


@dataclass
class BoundingBox:

    left: float
    upper: float
    right: float
    lower: float

    def as_tuple(self) -> Tuple[float]:
        return self.left, self.upper, self.right, self.lower

    def contains(self, other: BoundingBox) -> bool:
        return (
            self.left <= other.left
            and self.upper >= other.upper
            and self.right >= other.upper
            and self.lower <= other.lower
        )

    def __add__(self, other):
        return BoundingBox(
            min(self.left, other.left),
            max(self.upper, other.upper),
            max(self.right, other.right),
            min(self.lower, other.lower),
        )
