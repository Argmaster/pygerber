"""`static_rule` module contains definition of StaticRule class."""

from __future__ import annotations

from pygerber.gerber.ast.nodes import Node
from pygerber.gerber.linter.rules.rule import Rule


class StaticRule(Rule):
    """StaticRule class is a base class for simple rules requiring no dynamic messages
    and no logic except boolean triggered/not triggered check.
    """

    title: str
    description: str
    trigger_nodes: tuple[type[Node]]

    def get_violation_title(self) -> str:
        """Return a title of message that describes the rule violation."""
        return self.title

    def get_violation_description(self) -> str:
        """Return a description of the rule violation."""
        return self.description

    def get_trigger_nodes(self) -> list[type[Node]]:
        """Return a list of node names that trigger the rule."""
        return list(self.trigger_nodes)

    def node_callback(self, node: Node) -> None:
        """Check the node for violations."""
        self.report_violation(node.source_info)
