"""Parser level abstraction of draw operation which utilizes apertures for Gerber AST
parser, version 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from pydantic import Field

from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.attributes2 import ObjectAttributes
from pygerber.gerberx3.parser2.commands2.command2 import Command2

if TYPE_CHECKING:
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class ApertureDrawCommand2(Command2):
    """Parser level abstraction of draw operation for Gerber AST parser, version 2."""

    attributes: ObjectAttributes = Field(default_factory=ObjectAttributes)
    aperture: Aperture2

    def render_iter(self, hooks: Renderer2) -> Generator[Command2, None, None]:
        """Render draw operation."""
        self.render(hooks)
        yield self

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}()"
