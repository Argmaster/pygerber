"""`layer` module contains commands for image layer management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.box import Box
from pygerber.vm.types.layer_id import LayerID

if TYPE_CHECKING:
    from typing_extensions import Self


class StartLayer(Command):
    """Draw a line from the current position to the given position."""

    id: LayerID
    box: Box

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit start layer command."""
        visitor.on_start_layer(self)

    @classmethod
    def new(cls, id_: str, box: Box) -> Self:
        """Create a new start layer command from values."""
        return cls(
            id=LayerID(id=id_),
            box=box,
        )


class EndLayer(Command):
    """Draw a line from the current position to the given position."""

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit end layer command."""
        visitor.on_end_layer(self)
