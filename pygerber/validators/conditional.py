# -*- coding: utf-8 -*-
from typing import Any

from .validator import Validator


class CallOnCondition(Validator):
    def __init__(
        self, validator: Validator, condition: callable, onfailure: callable
    ) -> None:
        self.validator = validator
        self.condition = condition
        self.onfailure = onfailure

    def __call__(self, token, value: str) -> Any:
        cleaned_value = self.validator(token, value)
        if self.condition(token, cleaned_value):
            self.onfailure(token, cleaned_value)
        return cleaned_value
