"""The `errors` module provides error classes for the language server feature."""

from __future__ import annotations


class LanguageServerError(Exception):
    """Base class for language server errors."""


class LanguageServerNotAvailableError(LanguageServerError):
    """Language server feature requires pygerber[language-server] extras."""
