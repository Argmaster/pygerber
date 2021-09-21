# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable

from .validator import Validator

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState
    from pygerber.tokens.token import Token


class Float(Validator):
    def __call__(self, token: Token, drawing_state: DrawingState, value: str) -> float:
        if value is not None:
            return float(value)
        else:
            return self.default


class Int(Validator):
    def __call__(self, token: Token, drawing_state: DrawingState, value: str) -> int:
        if value is not None:
            return int(value)
        else:
            return self.default


class String(Validator):
    def __call__(self, token: Token, drawing_state: DrawingState, value: str) -> str:
        if value is not None:
            return str(value)
        else:
            return self.default


class Function(Validator):
    def __init__(self, function: Callable) -> None:
        self.function = function
        super().__init__(default=None)

    def __call__(self, token: Token, drawing_state: DrawingState, value: str) -> str:
        return self.function(token, value)
