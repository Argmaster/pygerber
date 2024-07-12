"""`layer` module contains commands for image layer management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.box import Box
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector

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


class PasteLayer(Command):
    """Paste contents of one layer into other layer."""

    id: LayerID

    center: Vector
    target_id: LayerID

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit paste layer command."""
        visitor.on_paste_layer(self)

    @classmethod
    def new(cls, id_: str, center: tuple[float, float], target_id: str) -> Self:
        """Create a new start layer command from values."""
        return cls(
            id=LayerID(id=id_),
            center=Vector.from_tuple(center),
            target_id=LayerID(id=target_id),
        )
