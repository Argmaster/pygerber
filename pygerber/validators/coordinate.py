# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .validator import Validator

from pygerber.tokens import token as tkn


class Coordinate(Validator):
    def __init__(self) -> None:
        super().__init__(default=None)

    def __call__(self, token: tkn.Token, value: str) -> Any:
        if value is not None:
            return token.meta.coparser.parse(value)
        else:
            return self.default
