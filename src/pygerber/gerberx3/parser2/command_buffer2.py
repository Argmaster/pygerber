"""Module contains definition of class for buffering draw commands."""
from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, Iterator, List, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.commands2.command2 import Command2

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.parser2.context2 import Parser2Context


class CommandBuffer2:
    """Container for buffering draw commands."""

    def __init__(self, commands: Optional[list[Command2]] = None) -> None:
        self.commands: list[Command2] = [] if commands is None else commands

    @classmethod
    def factory(cls, context: Parser2Context) -> Self:  # noqa: ARG003
        """CommandBuffer2 factory."""
        return cls(commands=[])

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

    commands: List[Command2] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return length of buffered commands."""
        return len(self.commands)

    def __iter__(self) -> Iterator[Command2]:  # type: ignore[override]
        """Iterate over buffered draw commands."""
        yield from self.commands

    def debug_buffer_to_json(self, indent: int = 4) -> str:
        """Convert buffered draw commands to JSON."""
        command_chain = ",\n".join(c.command_to_json() for c in self)
        return f"[\n{textwrap.indent(command_chain, ' ' * indent)}\n]"
