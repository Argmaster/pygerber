"""In-macro expression token."""

from __future__ import annotations

from pygerber.gerberx3.tokenizer.tokens.macro.element import Element


class Expression(Element):
    """Wrapper for in-macro expression."""

    def __init__(self) -> None:
        """Initialize token object."""
        super().__init__()
