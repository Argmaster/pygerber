"""`linter` module contains Linter class implementation."""

from __future__ import annotations

from typing import Iterable

from pygerber.gerber.ast.nodes.file import File
from pygerber.gerber.linter.event_ast_visitor import EventAstVisitor
from pygerber.gerber.linter.rule_violation import RuleViolation
from pygerber.gerber.linter.rules.rule import Rule
from pygerber.gerber.linter.violation_collector import ViolationCollector


class Linter:
    """Linter class implements high level linting API for Gerber files."""

    def __init__(self, rules: list[Rule]) -> None:
        """Initialize the Linter object."""
        self.rules = rules

    def _register_rule(self, rule: Rule) -> None:
        """Register a rule with the linter."""
        rule.bind_rule_to_ast_visitor(self.event_ast_visitor)
        rule.bind_rule_to_violation_collector(self.violation_collector)

    def lint(self, ast: File) -> Iterable[RuleViolation]:
        """Lint the AST and return a object containing all violations."""
        self.violation_collector = ViolationCollector()
        self.event_ast_visitor = EventAstVisitor()

        for rule in self.rules:
            rule.reset()
            self._register_rule(rule)

        ast.visit(self.event_ast_visitor)
        return self.violation_collector.violations
