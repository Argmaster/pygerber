# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from pygerber.validators.basic import String

from .token import Deprecated, Token


class G04_Token(Token):
    STRING = String("")

    regex = re.compile(r"G04(?P<STRING>.*?)\*")


@Deprecated("The single-quadrant mode G74 was deprecated in 2021.")
class G74_Token(Token):

    regex = re.compile(r"G74\*")


class G75_Token(Token):

    regex = re.compile(r"G75\*")


@Deprecated("LN was intended to be a human-readable comment. Use G04 command instead.")
class LoadName_Token(Token):
    regex = re.compile(r"%LN.*?\*%", re.DOTALL)
