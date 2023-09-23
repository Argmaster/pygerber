"""Wrapper for G74 token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.group import TokenGroup


class Statement(TokenGroup):
    """Wrapper for statement token group (%<something>%)."""

    def get_gerber_code(
        self,
        indent: str = "",
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return "%" + "".join(t.get_gerber_code(indent) for t in self.tokens) + "%"
