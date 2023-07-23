"""Simple of 2D vector container class."""

from __future__ import annotations

import operator
from decimal import Decimal
from typing import Callable

from pydantic import BaseModel, ConfigDict

from pygerber.backend.abstract.offset import Offset


class Vector2D(BaseModel):
    """Tuple wrapper for representing size with custom accessors."""

    model_config = ConfigDict(frozen=True)

    x: Offset
    y: Offset

    def as_pixels(self, dpi: int) -> tuple[int, int]:
        """Return size as pixels using given DPI for conversion."""
        return (self.x.as_pixels(dpi) or 1, self.y.as_pixels(dpi) or 1)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def _operator(
        self,
        other: object,
        op: Callable,
    ) -> Vector2D:
        if isinstance(other, Offset):
            return Vector2D(
                x=op(self.x, other),
                y=op(self.y, other),
            )
        if isinstance(other, Vector2D):
            return Vector2D(
                x=op(self.x, other.x),
                y=op(self.y, other.y),
            )

        if isinstance(other, (Decimal, int, float, str)):
            return Vector2D(
                x=op(self.x, Decimal(other)),
                y=op(self.y, Decimal(other)),
            )
        return NotImplemented  # type: ignore[unreachable]

    def __add__(self, other: object) -> Vector2D:
        return self._operator(other, operator.add)

    def __sub__(self, other: object) -> Vector2D:
        return self._operator(other, operator.sub)

    def __mul__(self, other: object) -> Vector2D:
        return self._operator(other, operator.mul)

    def __truediv__(self, other: object) -> Vector2D:
        return self._operator(other, operator.truediv)

    def __neg__(self) -> Vector2D:
        return Vector2D(x=-self.x, y=-self.y)

    def _i_operator(
        self,
        other: object,
        op: Callable,
    ) -> Vector2D:
        if isinstance(other, Vector2D):
            return self.model_copy(
                update={
                    "x": op(self.x, other.x),
                    "y": op(self.y, other.y),
                },
            )
        if isinstance(other, Offset):
            return self.model_copy(
                update={
                    "x": op(self.x, other),
                    "y": op(self.y, other),
                },
            )
        if isinstance(other, (Decimal, int, float, str)):
            return self.model_copy(
                update={
                    "x": op(self.x, Decimal(other)),
                    "y": op(self.y, Decimal(other)),
                },
            )
        return NotImplemented  # type: ignore[unreachable]

    def __iadd__(self, other: object) -> Vector2D:
        return self._i_operator(other, operator.add)

    def __isub__(self, other: object) -> Vector2D:
        return self._i_operator(other, operator.sub)

    def __imul__(self, other: object) -> Vector2D:
        return self._i_operator(other, operator.mul)

    def __itruediv__(self, other: object) -> Vector2D:
        return self._i_operator(other, operator.truediv)

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}(x={self.x}, y={self.y})"
