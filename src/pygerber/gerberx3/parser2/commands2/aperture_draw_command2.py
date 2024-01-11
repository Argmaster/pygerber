"""Parser level abstraction of draw operation which utilizes apertures for Gerber AST
parser, version 2.
"""
from __future__ import annotations

from pydantic import Field

from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.attributes2 import ObjectAttributes
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID


class ApertureDrawCommand2(Command2):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    attributes: ObjectAttributes = Field(default_factory=ObjectAttributes)
    aperture_id: ApertureID

    def get_aperture(self) -> Aperture2:
        """Get aperture."""
        return self.state.get_aperture(self.aperture_id)

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"
