# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.exceptions import EndOfStream
import re

from pygerber.validators import load_validators

from .token import Token


@load_validators
class EndOfStream_Token(Token):
    regex = re.compile(r"M02\*")

    def affect_meta(self):
        raise EndOfStream()

@load_validators
class Whitespace_Token(Token):
    regex = re.compile(r"\s+")
    keep: bool = False

