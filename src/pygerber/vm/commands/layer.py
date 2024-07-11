"""`layer` module contains commands for image layer management."""

from __future__ import annotations

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.point import Point


class StartLayer(Command):
    """Draw a line from the current position to the given position."""

    id: LayerID

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit start layer command."""
        visitor.on_start_layer(self)


class EndLayer(Command):
    """Draw a line from the current position to the given position."""

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit end layer command."""
        visitor.on_end_layer(self)


class PasteLayer(Command):
    """Paste contents of one layer into other layer."""

    id: LayerID

    center: Point
    target_id: LayerID

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit paste layer command."""
        visitor.on_paste_layer(self)
