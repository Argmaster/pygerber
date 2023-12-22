"""PyGerber's Gerber language server implementation."""

from __future__ import annotations

import importlib.util

IS_LANGUAGE_SERVER_FEATURE_AVAILABLE: bool = False

try:
    _spec_pygls = importlib.util.find_spec("pygls")
    _spec_lsprotocol = importlib.util.find_spec("lsprotocol")

    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE = (_spec_pygls is not None) and (
        _spec_lsprotocol is not None
    )
except (ImportError, ValueError):
    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE = False
