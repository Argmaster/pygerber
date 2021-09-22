# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygerber.drawing_state import DrawingState

import re

from pygerber.validators.basic import Float, String

from .token import Token


class LoadPolarityToken(Token):
    regex = re.compile(r"%LP(?P<POLARITY>[CD])\*%")

    POLARITY = String()

    def alter_state(self, state: DrawingState):
        state.set_polarity(self.POLARITY)


class LoadMirroringToken(Token):
    regex = re.compile(r"%LM(?P<MIRRORING>((N)|(X)|(Y)|(XY)))\*%")

    MIRRORING = String()

    def alter_state(self, state: DrawingState):
        state.set_mirroring(self.MIRRORING)



class LoadRotationToken(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*\.?[0-9]*"

    regex = re.compile(r"%LR(?P<ROTATION>{0})\*%".format(FLOAT_PATTERN))

    ROTATION = Float()

    def alter_state(self, state: DrawingState):
        state.set_rotation(self.ROTATION)



class LoadScalingToken(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*\.?[0-9]*"

    regex = re.compile(r"%LS(?P<SCALE>{0})\*%".format(FLOAT_PATTERN))

    SCALE = Float()

    def alter_state(self, state: DrawingState):
        state.set_scaling(self.SCALE)



class LoadUnitToken(Token):

    regex = re.compile(r"%MO(?P<UNIT>(MM)|(IN))\*%")

    UNIT = String()

    def alter_state(self, state: DrawingState):
        state.set_unit(self.UNIT)
