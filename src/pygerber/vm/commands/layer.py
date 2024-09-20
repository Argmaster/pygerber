"""`layer` module contains commands for image layer management."""

from __future__ import annotations

from typing import Optional

from pydantic import Field

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.box import Box
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector


class StartLayer(Command):
    """Draw a line from the current position to the given position."""

    id: LayerID
    box: Optional[Box] = Field(default=None)
    origin: Vector = Field(default_factory=lambda: Vector(x=0, y=0))

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit start layer command."""
        visitor.on_start_layer(self)


class EndLayer(Command):
    """Draw a line from the current position to the given position."""

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit end layer command."""
        visitor.on_end_layer(self)
