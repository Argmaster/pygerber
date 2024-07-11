"""`command_visitor` module contains definition of `CommandVisitor` interface.

For more information on the visitor pattern used here, visit:
https://refactoring.guru/design-patterns/visitor
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.vm.commands.layer import EndLayer, PasteLayer, StartLayer
    from pygerber.vm.commands.polygon import Polygon


class CommandVisitor:
    """Interface of a command visitor."""

    def on_polygon(self, command: Polygon) -> None:
        """Visit polygon command."""

    def on_start_layer(self, command: StartLayer) -> None:
        """Visit start layer command."""

    def on_end_layer(self, command: EndLayer) -> None:
        """Visit start end command."""

    def on_paste_layer(self, command: PasteLayer) -> None:
        """Visit paste layer command."""
