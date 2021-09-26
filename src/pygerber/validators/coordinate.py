# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState

from pygerber.constants import Unit
from pygerber.tokens import token as tkn

from .validator import Validator

INCH_TO_MM_RATIO = 25.4


class Coordinate(Validator):
    def __init__(self) -> None:
        super().__init__(default=None)

    def __call__(self, token: tkn.Token, state: DrawingState, value: str) -> Any:
        value = self.parse(state, value)
        if value is not None:
            value = self.ensure_mm(state, value)
        return value

    def parse(self, state: DrawingState, value: str) -> Any:
        if value is not None:
            return state.parse_co(value)

    def ensure_mm(self, state: tkn.Token, value: float):
        if state.unit == Unit.INCHES:
            return value * INCH_TO_MM_RATIO
        else:
            return value


class UnitFloat(Coordinate):
    def __init__(self, default: float = None) -> None:
        self.default = default

    def __call__(self, token: tkn.Token, state: DrawingState, value: str) -> Any:
        if value is not None:
            return self.ensure_mm(state, float(value))
        else:
            return self.default
