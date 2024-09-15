"""`command_visitor` module contains definition of `CommandVisitor` interface.

For more information on the visitor pattern used here, visit:
https://refactoring.guru/design-patterns/visitor
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.vm.commands import EndLayer, PasteLayer, Shape, StartLayer


class CommandVisitor:
    """Interface of a command visitor."""

    def on_shape(self, command: Shape) -> None:
        """Visit `Shape` command."""

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit `StartLayer` command."""

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit `EndLayer` command."""

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit `PasteLayer` command."""
