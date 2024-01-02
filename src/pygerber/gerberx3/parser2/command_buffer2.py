"""Module contains definition of class for buffering draw commands."""
from __future__ import annotations

from typing import Iterator, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.commands2.command2 import Command2


class CommandBuffer2:
    """Container for buffering draw commands."""

    def __init__(self, commands: Optional[list[Command2]] = None) -> None:
        self.commands: list[Command2] = [] if commands is None else commands

    def add_command(self, __command: Command2) -> None:
        """Add draw command to command buffer."""
        self.commands.append(__command)

    def get_readonly(self) -> ReadonlyCommandBuffer2:
        """Make buffer read-only."""
        return ReadonlyCommandBuffer2(commands=self.commands)

    def copy(self) -> CommandBuffer2:
        """Create copy of command buffer."""
        return CommandBuffer2(commands=self.commands.copy())

    def __iter__(self) -> Iterator[Command2]:
        """Iterate over buffered draw commands."""
        yield from self.commands


class ReadonlyCommandBuffer2(FrozenGeneralModel):
    """Read only command buffer proxy."""

    commands: list[Command2] = Field(default_factory=list)
