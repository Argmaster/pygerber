# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from pygerber.meta.meta import Unit
from pygerber.tokens import token as tkn

from .validator import Validator

INCH_TO_MM_RATIO = 25.4


class Coordinate(Validator):
    def __init__(self) -> None:
        super().__init__(default=None)

    def __call__(self, token: tkn.Token, value: str) -> Any:
        return self.replace_none_with_valid(
            token, self.parse(token, value),
        )

    def parse(self, token: tkn.Token, value: str) -> Any:
        if value is not None:
            return token.meta.coparser.parse(value)

    def ensure_mm(self, token: tkn.Token, value: float):
        if token.meta.unit == Unit.INCHES:
            return value * INCH_TO_MM_RATIO
        else:
            return value

    def replace_none_with_valid(self, token: tkn.Token, value: float):
        if value is None:
            return self.get_default(token)
        else:
            return self.ensure_mm(token, value)

    def get_default(self, token: tkn.Token):
        raise TypeError(
            "get_default(...) not implemented. Implement it in subclass or use VectorCoordinateX, "
            "VectorCoordinateY, OffsetCoordinate instead."
        )


class VectorCoordinateX(Coordinate):
    def get_default(self, token: tkn.Token):
        return token.get_current_point().x


class VectorCoordinateY(Coordinate):
    def get_default(self, token: tkn.Token):
        return token.get_current_point().y


class OffsetCoordinate(Coordinate):
    def get_default(self, token: tkn.Token):
        return 0

class UnitFloat(Coordinate):
    def __init__(self, default: float = None) -> None:
        self.default = default

    def __call__(self, token: tkn.Token, value: str) -> Any:
        if value is not None:
            return self.ensure_mm(token, float(value))
        else:
            return self.default
