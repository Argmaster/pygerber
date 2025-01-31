"""`rule_violation` contains the RuleViolation class."""

from __future__ import annotations

from pydantic import BaseModel


class RuleViolation(BaseModel):
    """Represents a rule violation detected by the linter."""

    rule_id: str
    title: str
    description: str
    start_offset: int
    end_offset: int
