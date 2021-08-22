# -*- coding: utf-8 -*-
from __future__ import annotations
from pygerber.validators.basic import String
from pygerber.exceptions import EndOfStream
import re

from pygerber.validators import load_validators

from .token import Token


@load_validators
class ApertureMacro_Token(Token):
    regex = re.compile(r"%AM(?P<NAME>.*?)\*(?P<BODY>.*?)\*%", re.DOTALL)

    NAME = String()
    BODY = String()
