from __future__ import annotations

import re
from .token import Token


class D01_Token(Token):
    regex = re.compile(r"X(?P<X>-?[0-9]+)?")
    X: int
    Y: int
    I: int
    J: int