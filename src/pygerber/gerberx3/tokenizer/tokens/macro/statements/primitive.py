"""Macro primitives tokens."""

from __future__ import annotations

from typing import ClassVar

from pygerber.gerberx3.tokenizer.tokens.macro.statements.statement import (
    MacroStatementToken,
)


class MacroPrimitiveToken(MacroStatementToken):
    """Wrapper for macro primitive token, common base class for specialized tokens."""

    symbol: ClassVar[str] = "X"
