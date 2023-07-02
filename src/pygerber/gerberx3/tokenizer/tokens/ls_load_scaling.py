"""Wrapper for load scaling token."""
from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.token import Token


class LoadScaling(Token):
    """Wrapper for load scaling token.

    Loads the scaling object transformation parameter.
    """

    def __init__(self, scaling: str) -> None:
        """Initialize token object."""
        super().__init__()
        self.scaling = float(scaling)

    def __str__(self) -> str:
        """Return pretty representation of comment token."""
        return f"LS{self.scaling}*"
