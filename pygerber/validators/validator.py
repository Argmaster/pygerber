# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState
    from pygerber.tokens.token import Token

from typing import Any


class Validator:
    def __init__(self, default: Any = None) -> None:
        self.default = default

    def __call__(self, token: Token, state: DrawingState, value: str) -> str:
        return value
