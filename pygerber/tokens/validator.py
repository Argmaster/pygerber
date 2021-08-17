from __future__ import annotations

import re
from typing import Dict, TYPE_CHECKING, Any, Callable

from pygerber.exceptions import InvalidCommandFormat, suppress_context

if TYPE_CHECKING:
    from pygerber.tokens.token import Token


def load_validators(class_):
    class_.validators = {}
    for key in class_.__dict__.keys():
        value = class_.__dict__.get(key)
        if isinstance(value, Validator):
            class_.validators[key] = value
    return class_

class Validator:
    def __init__(self, default: Any = None) -> None:
        self.default = default

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


class ValidatorDispatcher:
    validators: Dict[str, Validator]

    def dispatch(self, meta) -> None:
        self.meta = meta
        group_dict = self.get_groupdict()
        for attribute_name, validator in self.validators.items():
            try:
                value = group_dict.get(attribute_name, None)
                cleaned_value = validator(self, value)
                setattr(self, attribute_name, cleaned_value)
            except ValueError as e:
                self.raise_invalid_format(e.__str__())

    def get_groupdict(self) -> dict:
        if self.re_match is not None:
            return self.re_match.groupdict()
        else:
            return {}


    def raise_invalid_format(self, message):
        raise suppress_context(
            InvalidCommandFormat(
                f"Failed to dispatch expression `{self.re_match.group()}`, {message}"
            )
        )


class Dispatcher(ValidatorDispatcher, Validator):

    re_match: re.Match

    def __init__(self, pattern: str | Callable) -> None:
        self.pattern = pattern

    def get_pattern(self, token, value) -> re.Pattern:
        if callable(self.pattern):
            return self.pattern(token, value)
        else:
            return self.pattern

    def __call__(self, token: Token, value: str) -> str:
        if value is not None:
            pattern = self.get_pattern(token, value)
            self.re_match = pattern.match(value)
            if self.re_match is None:
                raise InvalidCommandFormat(f"Invalid set of arguments.")
        else:
            self.re_match = None
        self.dispatch(token.meta)
        return self
