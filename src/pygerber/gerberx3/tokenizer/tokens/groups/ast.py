"""Wrapper for G74 token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.group import TokenGroup


class AST(TokenGroup):
    """Gerber format abstract syntax tree."""
