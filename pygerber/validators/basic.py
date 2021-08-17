# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from .validator import Validator

if TYPE_CHECKING:
    from pygerber.tokens.token import Token


class Float(Validator):
    def __call__(self, token: Token, value: str) -> float:
        if value is not None:
            return float(value)
        else:
            return self.default


class Int(Validator):
    def __call__(self, token: Token, value: str) -> int:
        if value is not None:
            return int(value)
        else:
            return self.default


class String(Validator):
    def __call__(self, token: Token, value: str) -> str:
        if value is not None:
            return str(value)
        else:
            return self.default
