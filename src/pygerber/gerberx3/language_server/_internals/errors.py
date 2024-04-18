"""All language server specific error classes."""

from __future__ import annotations


class LanguageServerError(RuntimeError):
    """Base class for errors raised by language server."""


class EmptyASTError(LanguageServerError):
    """Error raised when AST is empty."""
