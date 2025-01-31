"""`violation_collector` module contains the ViolationCollector class."""

from __future__ import annotations

from pygerber.gerber.linter.rule_violation import RuleViolation


class ViolationCollector:
    """ViolationCollector class is a container for RuleViolations."""

    def __init__(self) -> None:
        """Initialize the ViolationCollector object."""
        self.violations: list[RuleViolation] = []

    def add_violation(self, violation: RuleViolation) -> None:
        """Add a violation to the collector."""
        self.violations.append(violation)
