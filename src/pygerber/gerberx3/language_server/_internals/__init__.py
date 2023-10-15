"""PyGerber's Gerber language server implementation."""

from __future__ import annotations

import importlib.util

IS_LANGUAGE_SERVER_FEATURE_AVAILABLE: bool

try:
    importlib.util.find_spec("pygls")
except ImportError:
    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE = False
else:
    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE = True
