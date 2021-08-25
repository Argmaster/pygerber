# -*- coding: utf-8 -*-
from __future__ import annotations
from abc import abstractmethod
from pygerber.meta.meta import Unit

from typing import TYPE_CHECKING, Any

from .validator import Validator

from pygerber.tokens import token as tkn


INCH_TO_MM_RATIO = 25.4


class Coordinate(Validator):
    def __init__(self, use_x=True, use_y=False) -> None:
        self.use_x = use_x
        self.use_y = use_y
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
            return self.get_default(token, value)
        else:
            return self.ensure_mm(token, value)

    @abstractmethod
    def get_default(self, token: tkn.Token, value: float):
        raise TypeError(
            "get_default not implemented. Implement it in subclass or use VectorCoordinateX, "
            "VectorCoordinateY, OffsetCoordinate instead."
        )


class VectorCoordinateX(Coordinate):
    def get_default(self, token: tkn.Token, value: float):
        return token.meta.current_point.x


class VectorCoordinateY(Coordinate):
    def get_default(self, token: tkn.Token, value: float):
        return token.meta.current_point.y


class OffsetCoordinate(Coordinate):
    def get_default(self, token: tkn.Token, value: float):
        return 0

class UnitFloat(Coordinate):
    def __init__(self, default: float = None) -> None:
        self.default = default

    def __call__(self, token: tkn.Token, value: str) -> Any:
        if value is not None:
            return self.ensure_mm(token, float(value))
        else:
            return self.default
