"""`DEP001` module contains linter rule DEP001 implementation."""  # noqa: N999

from __future__ import annotations

from pygerber.gerber.ast.nodes import G54
from pygerber.gerber.linter.rules.rule import register_rule
from pygerber.gerber.linter.rules.static_rule import StaticRule


@register_rule
class DEP001(StaticRule):
    """Rule DEP001 class implements a specific linting rule."""

    rule_id = "DEP001"
    title = "Use of deprecated G54 code."
    description = (
        "This historic code optionally precedes an aperture "
        "selection Dnn command. It has no effect. "
        "Sometimes used. Deprecated in 2012."
    )
    trigger_nodes = (G54,)
