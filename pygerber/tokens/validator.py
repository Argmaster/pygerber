from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pygerber.tokens.token import Token


class Validator(ABC):
    def __init__(self, default: Any = None) -> None:
        self.default = default

    @abstractmethod
    def __call__(self, token: Token, value: str) -> str:
        pass


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


class Coordinate(Validator):
    def __init__(self) -> None:
        super().__init__(default=None)

    def __call__(self, token: Token, value: str) -> Any:
        if value is not None:
            return token.meta.coparser.parse(value)
        else:
            return self.default


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
