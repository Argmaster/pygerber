"""`GRB001` module contains linter rule GRB001 implementation."""  # noqa: N999

from __future__ import annotations

from pygerber.gerber.ast.nodes import G01, G02, G03, ABclose, Node
from pygerber.gerber.linter.rules.rule import Rule, register_rule


@register_rule
class GRB001(Rule):
    """Rule GRB001 class implements a specific linting rule."""

    rule_id = "GRB001"
    last_node: type[Node] | None = None

    def get_violation_title(self) -> str:
        """Return a title of message that describes the rule violation."""
        assert self.last_node is not None
        return f"""Redundant {self.last_node.__qualname__} command."""

    def get_violation_description(self) -> str:
        """Return a description of the rule violation."""
        assert self.last_node is not None
        return (
            f"The {self.last_node.__qualname__} command after once issued "
            "remains in effect until different G01/G02/G03 command changes "
            " the interpolation mode. Some software tends to paste G01 command "
            "before each D01 command, significantly increasing the file size."
        )

    def get_trigger_nodes(self) -> list[type[Node]]:
        """Return a list of node names that trigger the rule."""
        return [G01, G02, G03, ABclose]

    def node_callback(self, node: Node) -> None:
        """Check the node for violations."""
        if isinstance(node, (G01, G02, G03)) and self.last_node == node.__class__:
            self.report_violation(node.source_info)

        self.last_node = node.__class__

    def reset(self) -> None:
        """Reset the rule state."""
        self.last_node = None
