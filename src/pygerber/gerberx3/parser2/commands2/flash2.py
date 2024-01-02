"""Parser level abstraction of flash operation for Gerber AST parser, version 2."""
from __future__ import annotations

from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.tokenizer.aperture_id import ApertureID


class Flash2(Command2):
    """Parser level abstraction of flash operation for Gerber AST parser,
    version 2.
    """

    aperture_id: ApertureID
    flash_point: Vector2D
