"""Parser level abstraction of macro aperture info for Gerber AST parser, version 2."""

from __future__ import annotations

from pygerber.gerberx3.parser2.apertures2.aperture2 import Aperture2
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2


class Macro2(Aperture2):
    """Parser level abstraction of aperture info for macro aperture."""

    command_buffer: ReadonlyCommandBuffer2
