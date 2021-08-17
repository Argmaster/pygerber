# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

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
    def match(class_: Token, source: str, index: int = 0) -> Token:
        optional_match = class_.regex.match(source, pos=index)
        if optional_match is None:
            return False
        else:
            # Token object have to be dispatched to make it functional
            return class_(optional_match)

    def affect_meta(self):
        """
        This method should be called only after token is dispatched and before evaluate().
        """
        pass

    def evaluate(self):
        """
        This method should be called only after token is dispatched and after affect_meta().
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
