# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from types import SimpleNamespace
from typing import TYPE_CHECKING, Callable

from pygerber.tokens.dispatcher_meta import Dispatcher

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState
    from pygerber.tokens.token import Token

from pygerber.exceptions import InvalidCommandFormat

from .validator import Validator


class StructValidator(Dispatcher, Validator):

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

    def __call__(self, token: Token, state: DrawingState, value: str) -> str:
        if value is not None:
            return self.clean_args(token, state, value)
        else:
            return self.empty_namespace(token, state)

    def clean_args(self, token: Token, state: DrawingState, value: str):
        pattern = self.get_pattern(token, value)
        self.re_match = pattern.match(value)
        if self.re_match is None:
            raise InvalidCommandFormat("Invalid set of arguments.")
        namespace = SimpleNamespace(__validators__=self.__validators__)
        Dispatcher.__init__(namespace, self.re_match, state)
        return namespace

    def empty_namespace(self, token: Token, state: DrawingState):
        namespace = SimpleNamespace()
        for key, validator in self.__validators__:
            setattr(namespace, key, validator(token, state, None))
        return namespace
