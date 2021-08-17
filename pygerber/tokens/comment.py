# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from pygerber.validators import String, load_validators

from .token import Deprecated, Token


@load_validators
class G04Token(Token):
    STRING = String("")

    regex = re.compile(r"G04(?P<STRING>.*?)\*")


@Deprecated("The single-quadrant mode G74 was deprecated in 2021.")
@load_validators
class G74Token(Token):

    regex = re.compile(r"G74\*")


@load_validators
class G75Token(Token):

    regex = re.compile(r"G75\*")
