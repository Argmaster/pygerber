# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from pygerber.meta import Meta

import pygerber.validators as validator


class Token(validator.ValidatorDispatcher, metaclass=ABCMeta):
    regex: re.Pattern
    re_match: re.Match
    # meta attribute is only available after dispatch
    meta: Meta

    def __init__(self, match_object: re.Match) -> None:
        self.re_match = match_object

    @classmethod
    def match_and_dispatch(
        class_, meta: Meta, source: str, index: int = 0
    ) -> Union[Token, bool]:
        # returns False on failure, Token object on success, token is dispatched.
        token = class_.match(source, index)
        if token:
            token.dispatch(meta)
        return token

    @classmethod
    def match(class_: Token, source: str, index: int = 0) -> Union[Token, bool]:
        # returns False on failure, Token object on success, token is not dispatched.
        optional_match = class_.regex.match(source, pos=index)
        if optional_match is None:
            return False
        else:
            # Token object have to be dispatched to make it functional
            return class_(optional_match)

    def dump_co(self, co: float):
        return self.meta.coparser.dump(co)

    def affect_meta(self):
        """
        This method should be called only after token is dispatched and before render().
        """
        pass

    def render(self):
        """
        This method should be called only after token is dispatched and after affect_meta().
        """
        pass

    def __str__(self) -> str:
        """
        Construct string of Gerber code coresponding to data held in token.
        """
        return self.re_match.group()


class Deprecated:
    def __init__(self, message) -> None:
        self.message = message

    def __call__(self, class_: Token):
        message = self.message

        def deprecated_dispatch(self, meta):
            meta.raiseDeprecatedSyntax(message)
            super(class_, self).dispatch(meta)

        class_.dispatch = deprecated_dispatch

        return class_
