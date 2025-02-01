"""`rule` module contains the Rule class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Optional, TypeVar

from pygerber.gerber.ast.nodes import Node, SourceInfo
from pygerber.gerber.linter.event_ast_visitor import EventAstVisitor
from pygerber.gerber.linter.rule_violation import RuleViolation
from pygerber.gerber.linter.violation_collector import ViolationCollector


class Rule(ABC):
    """Base class for Gerber linter rules."""

    rule_id: ClassVar[str]
    collector: Optional[ViolationCollector] = None

    @abstractmethod
    def get_violation_title(self) -> str:
        """Return a title of message that describes the rule violation."""

    @abstractmethod
    def get_violation_description(self) -> str:
        """Return a description of the rule violation."""

    @abstractmethod
    def get_trigger_nodes(self) -> list[type[Node]]:
        """Return a list of node names that trigger the rule."""

    def bind_rule_to_ast_visitor(self, visitor: EventAstVisitor) -> None:
        """Bind the rule to the visitor."""
        for node_type in self.get_trigger_nodes():
            visitor.register_listener(node_type, self.node_callback)

    def bind_rule_to_violation_collector(self, collector: ViolationCollector) -> None:
        """Bind the rule to the violation collector."""
        self.collector = collector

    @abstractmethod
    def reset(self) -> None:
        """Reset the rule state."""

    def report_violation(self, source_info: Optional[SourceInfo]) -> None:
        """Report a violation."""
        if self.collector is not None:
            violation = RuleViolation(
                rule_id=self.rule_id,
                title=self.get_violation_title(),
                description=self.get_violation_description(),
                start_offset=(source_info.location if source_info is not None else 0),
                end_offset=(
                    source_info.location + source_info.length
                    if source_info is not None
                    else 0
                ),
                line=(source_info.line if source_info is not None else 0),
                column=(source_info.column if source_info is not None else 0),
            )
            self.collector.add_violation(violation)

    @abstractmethod
    def node_callback(self, node: Node) -> None:
        """Check the node for violations."""


RULE_REGISTRY: dict[str, type[Rule]] = {}

T = TypeVar("T", bound="Rule")


def register_rule(rule: type[T]) -> type[T]:
    """Register a rule with the linter."""
    assert rule.rule_id not in RULE_REGISTRY, f"Rule {rule.rule_id} already registered."
    RULE_REGISTRY[rule.rule_id] = rule
    return rule
