"""Basic types for AST nodes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

Double: TypeAlias = float
Integer: TypeAlias = int
