"""Module contains MacroContext class definition."""
from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field

from pygerber.backend.abstract.offset import Offset


class MacroContext(BaseModel):
    """Macro context object used during macro evaluation."""

    variables: Dict[str, Offset] = Field(default_factory=dict)
