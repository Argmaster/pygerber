"""Base class for attribute tokens."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.bases.extended_command import (
    ExtendedCommandToken,
)


class AttributeToken(ExtendedCommandToken):
    """Base class for all attribute manipulation tokens."""
