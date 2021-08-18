# -*- coding: utf-8 -*-
from __future__ import annotations

import re

from pygerber.validators import Float, String, load_validators

from .token import Token


@load_validators
class LoadPolarityToken(Token):
    regex = re.compile(r"%LP(?P<POLARITY>[CD])\*%")

    POLARITY = String()

    def affect_meta(self):
        self.meta.set_polarity(self.POLARITY)


@load_validators
class LoadMirroringToken(Token):
    regex = re.compile(r"%LM(?P<MIRRORING>((N)|(X)|(Y)|(XY)))\*%")

    MIRRORING = String()

    def affect_meta(self):
        self.meta.set_mirroring(self.MIRRORING)


@load_validators
class LoadRotationToken(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*\.?[0-9]*"

    regex = re.compile(r"%LR(?P<ROTATION>{0})\*%".format(FLOAT_PATTERN))

    ROTATION = Float()

    def affect_meta(self):
        self.meta.set_rotation(self.ROTATION)


@load_validators
class LoadScalingToken(Token):

    FLOAT_PATTERN = r"[-+]?[0-9]*\.?[0-9]*"

    regex = re.compile(r"%LS(?P<SCALE>{0})\*%".format(FLOAT_PATTERN))

    SCALE = Float()

    def affect_meta(self):
        self.meta.set_scaling(self.SCALE)


@load_validators
class LoadUnitToken(Token):

    regex = re.compile(r"%MO(?P<UNIT>(MM)|(IN))\*%")

    UNIT = String()

    def affect_meta(self):
        self.meta.set_unit(self.UNIT)
