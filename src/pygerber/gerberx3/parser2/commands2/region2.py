"""Parser level abstraction of draw region operation for Gerber AST parser,
version 2.
"""
from __future__ import annotations

from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.command2 import Command2


class Region2(Command2):
    """Parser level abstraction of draw region operation for Gerber AST parser,
    version 2.
    """

    command_buffer: ReadonlyCommandBuffer2
