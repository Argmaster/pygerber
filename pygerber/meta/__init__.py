from typing import Tuple

from pygerber.exceptions import DeprecatedSyntax

from .apertureset import ApertureSet
from .broker import DrawingBroker
from .coparser import CoParser
from .meta import Interpolation, Mirroring, Polarity, Unit


class Meta(DrawingBroker):

    coparser = CoParser

    def __init__(
        self,
        apertureSet: ApertureSet,
        *,
        ignore_deprecated: bool = True,
    ) -> None:
        super().__init__(apertureSet)
        self.ignore_deprecated = ignore_deprecated
        self.coparser = CoParser()

    def raiseDeprecatedSyntax(self, message: str):
        if not self.ignore_deprecated:
            raise DeprecatedSyntax(message)
