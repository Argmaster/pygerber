"""`static_rule` module contains definition of StaticRule class."""

from __future__ import annotations

from pygerber.gerber.ast.nodes import Node
from pygerber.gerber.linter.rules.rule import Rule


class StaticRule(Rule):
    """StaticRule class is a base class for simple rules requiring no dynamic messages
    and no logic except boolean triggered/not triggered check.
    """

    title: str
    message: str
    trigger_nodes: tuple[type[Node]]

    def get_violation_title(self) -> str:
        """Return a title of message that describes the rule violation."""
        return self.title

    def get_violation_description(self) -> str:
        """Return a description of the rule violation."""
        return self.message

    def get_trigger_nodes(self) -> list[type[Node]]:
        """Return a list of node names that trigger the rule."""
        return list(self.trigger_nodes)

    def node_callback(self, node: Node) -> None:
        """Check the node for violations."""
        self.report_violation(
            start_offset=(
                node.source_info.location if node.source_info is not None else 0
            ),
            end_offset=(
                node.source_info.location + node.source_info.length
                if node.source_info is not None
                else 0
            ),
        )
