"""Module contains definition of class for buffering draw commands."""
from __future__ import annotations

from typing import Iterator, List

from pydantic import Field

from pygerber.common.general_model import GeneralModel
from pygerber.gerberx3.parser2.draws2.draw2 import Draw2


class CommandBuffer2(GeneralModel):
    """Container for buffering draw commands."""

    commands: List[Draw2] = Field(default_factory=list)

    def add_command(self, __command: Draw2) -> None:
        """Add draw command to command buffer."""
        self.commands.append(__command)

    def get_commands(self) -> Iterator[Draw2]:
        """Get list of buffered draw commands."""
        yield from self.commands
