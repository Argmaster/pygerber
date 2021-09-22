# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState

from pygerber.constants import Unit
from pygerber.tokens import token as tkn

from .validator import Validator

INCH_TO_MM_RATIO = 25.4


class Coordinate(Validator):
    def __init__(self) -> None:
        super().__init__(default=None)

    def __call__(self, token: tkn.Token, drawing_state: DrawingState, value: str) -> Any:
        value = self.parse(drawing_state, value)
        value = self.ensure_mm(drawing_state, value)
        return value

    def parse(self, drawing_state: DrawingState, value: str) -> Any:
        if value is not None:
            return drawing_state.parse_co(value)

    def ensure_mm(self, drawing_state: tkn.Token, value: float):
        if drawing_state.unit == Unit.INCHES:
            return value * INCH_TO_MM_RATIO
        else:
            return value

class UnitFloat(Coordinate):
    def __init__(self, default: float = None) -> None:
        self.default = default

    def __call__(self, token: tkn.Token, drawing_state: DrawingState, value: str) -> Any:
        if value is not None:
            return self.ensure_mm(drawing_state, float(value))
        else:
            return self.default
