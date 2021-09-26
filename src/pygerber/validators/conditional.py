# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState
    from pygerber.tokens.token import Token

from .validator import Validator


class CallOnCondition(Validator):
    def __init__(
        self, validator: Validator, condition: callable, onfailure: callable
    ) -> None:
        self.validator = validator
        self.condition = condition
        self.onfailure = onfailure

    def __call__(self, token: Token, state: DrawingState, value: str) -> Any:
        cleaned_value = self.validator(token, state, value)
        if self.condition(token, cleaned_value):
            self.onfailure(token, cleaned_value)
        return cleaned_value
