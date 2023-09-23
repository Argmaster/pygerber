"""Wrapper for G74 token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class EndOfExpression(Token):
    """Wrapper for end of expression token (*)."""

    def get_gerber_code(
        self,
        indent: str = "",  # noqa: ARG002
        endline: str = "\n",  # noqa: ARG002
    ) -> str:
        """Get gerber code represented by this token."""
        return "*"
