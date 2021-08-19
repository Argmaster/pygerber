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


def outer(first, second) -> float:
    if abs(second) - abs(first) < 0:
        return second
    else:
        return first


@dataclass
class BoundingBox:

    xs: Tuple[float, float]
    ys: Tuple[float, float]

    @property
    def left_x(self):
        return min(self.xs)

    @property
    def top_y(self):
        return max(self.ys)

    @property
    def right_x(self):
        return max(self.xs)

    @property
    def bottom_y(self):
        return min(self.ys)

    def as_vectors(self) -> Tuple[Vector2D]:
        return (
            Vector2D(self.left_x, self.top_y),
            Vector2D(self.left_x, self.bottom_y),
        )

    def as_tuples(self) -> Tuple[Tuple[float, float]]:
        return (
            (self.left_x, self.top_y),
            (self.left_x, self.bottom_y),
        )

    def __add__(self, other: BoundingBox) -> BoundingBox:
        return BoundingBox(
            (
                outer(self.left_x, other.left_x),
                outer(self.top_y, other.top_y),
            ),
            (
                outer(self.right_x, other.right_x),
                outer(self.left_x, other.bottom_y),
            ),
        )
