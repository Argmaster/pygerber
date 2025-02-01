"""Code diagnostic logic."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

from pygerber.gerber.linter.event_ast_visitor import EventAstVisitor
from pygerber.gerber.linter.linter import Linter
from pygerber.gerber.linter.rule_violation import RuleViolation
from pygerber.gerber.linter.rules import (
    DEP001,
    DEP002,
    GRB001,
    RULE_REGISTRY,
    Rule,
    StaticRule,
)

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import File


def lint(ast: File, rules: Optional[list[str]] = None) -> Iterable[RuleViolation]:
    """Lint the AST using the provided rules.

    Parameters
    ----------
    ast : File
        Abstract syntax tree to lint.
    rules : list[str]
        List of rule names to apply, if empty or None, all rules are applied.

    Returns
    -------
    list[RuleViolation]
        List containing rule violations found in the AST.

    """
    if rules is not None and len(rules) != 0:
        rule_objects = [RULE_REGISTRY[rule_id]() for rule_id in rules]
    else:
        rule_objects = [r() for r in RULE_REGISTRY.values()]

    linter = Linter(rule_objects)
    return linter.lint(ast)


__all__ = [
    "DEP001",
    "DEP002",
    "GRB001",
    "RULE_REGISTRY",
    "EventAstVisitor",
    "Linter",
    "Rule",
    "RuleViolation",
    "StaticRule",
    "lint",
]
