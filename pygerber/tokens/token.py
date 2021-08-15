from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from pygerber.exceptions import DeprecatedSyntax, InvalidCommandFormat, suppress_context

if TYPE_CHECKING:
    from pygerber.meta import Meta


class Token(metaclass=ABCMeta):
    regex: re.Pattern
    re_match: re.Match
    # meta attribute is only available after dispatch
    meta: Meta

    def __init__(self, match_object: re.Match) -> None:
        self.re_match = match_object

    def dispatch(self, meta: Meta) -> None:
        """
        Dispatch named groups from match into instance attributes,
        should be called only once, before affect_meta and evaluate.
        Sets meta attribute on token instance.
        """
        self.meta = meta
        group_dict = self.re_match.groupdict()
        for attribute_name, value in group_dict.items():
            try:
                self.set_attribute(attribute_name, value)
            except ValueError as e:
                self.raise_invalid_format(self.re_match, e)

    def set_attribute(self, attribute_name, value):
        validator_function = getattr(self, attribute_name)
        setattr(self, attribute_name, validator_function(value))

    def raise_invalid_format(self, match_object, e):
        raise suppress_context(
            InvalidCommandFormat(
                f"Failed to dispatch expression `{match_object.group()}`, {e.__str__()}"
            )
        )

    @classmethod
    def match(class_: Token, source: str, index: int) -> Token:
        """
        Tries matching token regex against source, starting from index. On failure returns False,
        Token object otherwise. Token object should be dispatched to make it functional.
        """
        optional_match = class_.regex.match(source, pos=index)
        if optional_match is None:
            return False
        else:
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
