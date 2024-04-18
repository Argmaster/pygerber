"""Module contains definition of class for buffering draw commands."""

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, Iterator, List, Optional

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.math.vector_2d import Vector2D
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from decimal import Decimal

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

    def __getitem__(self, index: int) -> Command2:
        """Get item by index from commands."""
        return self.commands[index]


class ReadonlyCommandBuffer2(FrozenGeneralModel):
    """Read only command buffer proxy."""

    commands: List[Command2] = Field(default_factory=list)

    def __len__(self) -> int:
        """Return length of buffered commands."""
        return len(self.commands)

    def __iter__(self) -> Iterator[Command2]:  # type: ignore[override]
        """Iterate over buffered draw commands."""
        yield from self.commands

    def __getitem__(self, index: int) -> Command2:
        """Get item by index from commands."""
        return self.commands[index]

    def debug_buffer_to_json(self, indent: int = 4) -> str:
        """Convert buffered draw commands to JSON."""
        command_chain = ",\n".join(c.command_to_json() for c in self)
        return f"[\n{textwrap.indent(command_chain, ' ' * indent)}\n]"

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get new command buffer with all commands mirrored."""
        return self.model_copy(
            update={"commands": [c.get_mirrored(mirror) for c in self.commands]},
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get new command buffer with all commands transposed."""
        return self.model_copy(
            update={"commands": [c.get_transposed(vector) for c in self.commands]},
        )

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this command rotated around (0, 0)."""
        return self.model_copy(
            update={"commands": [c.get_rotated(angle) for c in self.commands]},
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        return self.model_copy(
            update={"commands": [c.get_scaled(scale) for c in self.commands]},
        )

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of command buffer."""
        bbox: Optional[BoundingBox] = None

        for command in self:
            if bbox is None:
                bbox = command.get_bounding_box()
            else:
                bbox += command.get_bounding_box()

        return BoundingBox.NULL if bbox is None else bbox
