"""Module contains definition of class for buffering draw commands."""
from __future__ import annotations

from typing import Iterator

from pygerber.gerberx3.parser2.commands2.command2 import Command2


class CommandBuffer2:
    """Container for buffering draw commands."""

    def __init__(self) -> None:
        self.commands = []

    def add_command(self, __command: Command2) -> None:
        """Add draw command to command buffer."""
        self.commands.append(__command)

    def __iter__(self) -> Iterator[Command2]:
        """Iterate over buffered draw commands."""
        yield from self.commands
