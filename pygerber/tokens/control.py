# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState
from pygerber.validators.basic import String
from pygerber.exceptions import EndOfStream
import re

from .token import Deprecated, Token


class EndOfStream_Token(Token):
    regex = re.compile(r"M0[02]\*")

    def alter_state(self, state: DrawingState):
        raise EndOfStream()


class Whitespace_Token(Token):
    regex = re.compile(r"\s+")
    keep: bool = False


@Deprecated(
    "This command has no effect in CAD to CAM "
    "workflows. Sometimes used, and then usually as "
    "%IPPOS*% to confirm the default and then it "
    "then has no effect. As it is not clear how "
    "%IPNEG*% must be handled it is probably a "
    "waste of time to try to fully implement it, and "
    "sufficient to give a warning on a %IPNEG*% and "
    "skip it. "
    "Deprecated in 2013"
)
class ImagePolarity_Token(Token):
    regex = re.compile(r"%IP(?P<POLARITY>((POS)|(NEG)))\*%")
    POLARITY = String("POS")
