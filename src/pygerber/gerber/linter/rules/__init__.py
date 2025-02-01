"""`rules` package contains all the linting rules for Gerber files."""

from __future__ import annotations

from pygerber.gerber.linter.rules.DEP001 import DEP001
from pygerber.gerber.linter.rules.DEP002 import DEP002
from pygerber.gerber.linter.rules.GRB001 import GRB001
from pygerber.gerber.linter.rules.rule import RULE_REGISTRY, Rule
from pygerber.gerber.linter.rules.static_rule import StaticRule

__all__ = ["DEP001", "DEP002", "GRB001", "RULE_REGISTRY", "Rule", "StaticRule"]
