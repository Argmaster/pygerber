# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from pygerber.validators.basic import String

from .token import Token


class ApertureMacro_Token(Token):
    regex = re.compile(r"%AM(?P<NAME>.*?)\*(?P<BODY>.*?)\*%", re.DOTALL)

    NAME = String()
    BODY = String()
