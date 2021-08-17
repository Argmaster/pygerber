from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pygerber.tokens.token import Token


class Validator:
    def __init__(self, default: Any = None) -> None:
        self.default = default

    def __call__(self, token: Token, value: str) -> str:
        return value


def load_validators(class_):
    class_.validators = {}
    for key in class_.__dict__.keys():
        value = class_.__dict__.get(key)
        if isinstance(value, Validator):
            class_.validators[key] = value
    return class_
