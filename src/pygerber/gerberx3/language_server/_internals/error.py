from __future__ import annotations


class LanguageServerNotAvailableError(RuntimeError):
    """Language server feature requires pygerber[language-server] extras."""
