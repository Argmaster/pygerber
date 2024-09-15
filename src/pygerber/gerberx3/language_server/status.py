"""The `is_server_available` module provides a boolean flag to check if the language
server feature is available.
"""

from __future__ import annotations

import importlib.util

from pygerber.gerberx3.language_server.errors import LanguageServerNotAvailableError


def is_language_server_available() -> bool:
    """Check if the language server feature is available."""
    try:
        _spec_pygls = importlib.util.find_spec("pygls")
        _spec_lsprotocol = importlib.util.find_spec("lsprotocol")

    except (ImportError, ValueError):
        return False

    else:
        return (_spec_pygls is not None) and (_spec_lsprotocol is not None)


def throw_if_server_not_available() -> None:
    """Raise an error if the language server feature is not available."""
    if not is_language_server_available():
        raise LanguageServerNotAvailableError
