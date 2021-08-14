from __future__ import annotations

import re
from abc import ABC
from typing import Union
from functools import cached_property


class Token(ABC):
    regex: re.Pattern
    string_match: re.Match

    def __init__(self, optional_match: str) -> None:
        self.string_match = optional_match

    def __bool__(self) -> bool:
        return self.string_match is not None

    @cached_property
    def string(self) -> str:
        return self.string_match.group()

    @classmethod
    def has_match(class_, source: str, begin: int=0) -> Union[bool, Token]:
        optional_match = class_.regex.match(source, pos=begin)
        return class_(optional_match)

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}<{self.string_match}>"

