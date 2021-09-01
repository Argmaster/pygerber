# -*- coding: utf-8 -*-
from __future__ import annotations

from pygerber.tokens.add import ADD_Token
from .aperture import Aperture


class CustomAperture(Aperture):
    def __init__(self, args: ADD_Token.ARGS, broker) -> None:
        self.broker = broker
        self.args = args
        self.process_args()

    def process_args(self):
        pass
