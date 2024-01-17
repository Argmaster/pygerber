"""Arithmetic expression token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.errors import TokenizerError


class InvalidArithmeticExpressionError(TokenizerError):
    """Raised when it's not possible to construct valid arithmetic expression."""
