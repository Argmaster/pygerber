from __future__ import annotations

import re
from types import SimpleNamespace
from typing import TYPE_CHECKING, Callable

from pygerber.exceptions import InvalidCommandFormat

from .validator import Validator
from .validator_dispatcher import ValidatorDispatcher

if TYPE_CHECKING:
    from pygerber.tokens.token import Token


class Dispatcher(ValidatorDispatcher, Validator):

    re_match: re.Match

    def __init__(self, pattern: str | Callable) -> None:
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern

    def get_pattern(self, token, value) -> re.Pattern:
        if callable(self.pattern):
            return self.pattern(token, value)
        else:
            return self.pattern


    def __call__(self, token: Token, value: str) -> str:
        if value is not None:
            return self.clean_not_none(token, value)
        else:
            return self.clean_none(token)

    def clean_not_none(self, token: Token, value: str):
        pattern = self.get_pattern(token, value)
        self.re_match = pattern.match(value)
        if self.re_match is None:
            raise InvalidCommandFormat(f"Invalid set of arguments.")
        return self.dispatch_into_namespace(token.meta)

    def clean_none(self, token: Token):
        self.re_match = None
        return self.dispatch_into_namespace(token.meta)

    def dispatch_into_namespace(self, meta):
        namespace = SimpleNamespace()
        return super().dispatch_into_namespace(meta, namespace)