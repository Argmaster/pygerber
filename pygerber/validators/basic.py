# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING

from .validator import Validator


from pygerber.tokens import token as tkn


class Float(Validator):
    def __call__(self, token: tkn.Token, value: str) -> float:
        if value is not None:
            return float(value)
        else:
            return self.default


class Int(Validator):
    def __call__(self, token: tkn.Token, value: str) -> int:
        if value is not None:
            return int(value)
        else:
            return self.default


class String(Validator):
    def __call__(self, token: tkn.Token, value: str) -> str:
        if value is not None:
            return str(value)
        else:
            return self.default
