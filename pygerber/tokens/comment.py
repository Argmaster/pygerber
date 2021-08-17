# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from .token import Token
from pygerber.validators import String, load_validators


@load_validators
class G04Token(Token):
    STRING = String("")

    regex = re.compile(r"G04(?P<STRING>.*?)\*")


class G75Token(Token):

    regex = re.compile(r"G75\*")