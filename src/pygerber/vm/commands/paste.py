"""`layer` module contains commands for image layer management."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from pygerber.vm.command_visitor import CommandVisitor
from pygerber.vm.commands.command import Command
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.types.vector import Vector

if TYPE_CHECKING:
    from typing_extensions import Self


class PasteLayer(Command):
    """Paste contents of one layer into other layer."""

    source_layer_id: LayerID
    center: Vector
    is_negative: bool = Field(default=False)

    def visit(self, visitor: CommandVisitor) -> None:
        """Visit paste layer command."""
        visitor.on_paste_layer(self)

    @classmethod
    def new(
        cls,
        source_layer_id: str,
        center: tuple[float, float],
        *,
        is_negative: bool = False,
    ) -> Self:
        """Create a new start layer command from values."""
        return cls(
            source_layer_id=LayerID(id=source_layer_id),
            center=Vector.from_tuple(center),
            is_negative=is_negative,
        )
