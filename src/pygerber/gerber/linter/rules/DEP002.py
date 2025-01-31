"""`DEP002` module contains linter rule DEP002 implementation."""  # noqa: N999

from __future__ import annotations

from pygerber.gerber.ast.nodes import G55
from pygerber.gerber.linter.rules.rule import register_rule
from pygerber.gerber.linter.rules.static_rule import StaticRule


@register_rule
class DEP002(StaticRule):
    """Rule DEP002 class implements a specific linting rule."""

    rule_id = "DEP002"
    title = "Use of deprecated G55 code."
    description = (
        "This historic code optionally precedes D03 code. It has no effect. "
        "Deprecated in 2012."
    )
    trigger_nodes = (G55,)
