"""Parser level abstraction of command that consists of multiple commands for Gerber AST
parser, version 2.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Iterator

from pygerber.gerberx3.math.bounding_box import BoundingBox
from pygerber.gerberx3.parser2.command_buffer2 import ReadonlyCommandBuffer2
from pygerber.gerberx3.parser2.commands2.command2 import Command2
from pygerber.gerberx3.state_enums import Mirroring

if TYPE_CHECKING:
    from decimal import Decimal

    from typing_extensions import Self

    from pygerber.gerberx3.math.vector_2d import Vector2D
    from pygerber.gerberx3.renderer2.abstract import Renderer2


class BufferCommand2(Command2):
    """Parser level abstraction of command that consists of multiple commands for Gerber
    AST parser, version 2.
    """

    command_buffer: ReadonlyCommandBuffer2

    def get_mirrored(self, mirror: Mirroring) -> Self:
        """Get mirrored command.

        Mirroring is a NOOP if mirror is `Mirroring.NoMirroring`.
        """
        if mirror == Mirroring.NoMirroring:
            return self
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_mirrored(mirror),
            },
        )

    def get_transposed(self, vector: Vector2D) -> Self:
        """Get transposed command."""
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_transposed(vector),
            },
        )

    def get_rotated(self, angle: Decimal) -> Self:
        """Get copy of this command rotated around (0, 0)."""
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_rotated(angle),
            },
        )

    def get_scaled(self, scale: Decimal) -> Self:
        """Get copy of this aperture scaled by factor."""
        return self.model_copy(
            update={
                "command_buffer": self.command_buffer.get_scaled(scale),
            },
        )

    def get_bounding_box(self) -> BoundingBox:
        """Get bounding box of draw operation."""
        return self.command_buffer.get_bounding_box()

    def render(self, renderer: Renderer2) -> None:
        """Render draw operation."""
        for _ in renderer.hooks.render_buffer(self):
            pass

    def render_iter(self, renderer: Renderer2) -> Generator[Command2, None, None]:
        """Render draw operation."""
        yield from renderer.hooks.render_buffer(self)

    def __len__(self) -> int:
        """Return length of buffered commands."""
        return len(self.command_buffer)

    def __iter__(self) -> Iterator[Command2]:  # type: ignore[override]
        """Iterate over buffered draw commands."""
        yield from self.command_buffer

    def __getitem__(self, index: int) -> Command2:
        """Get item by index from commands."""
        return self.command_buffer[index]
