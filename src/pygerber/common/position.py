"""Contains tools for expressing positions in text."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygerber.gerberx3.language_server._internals import (
    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE,
)

if TYPE_CHECKING:
    import lsprotocol.types as lspt
    from typing_extensions import Self

if IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:
    import lsprotocol.types as lspt


@dataclass
class Position:
    """Position of token in text in pyparsing scheme (lines starts from 1,
    columns also start from 1).
    """

    line: int
    column: int

    @classmethod
    def from_vscode_position(cls, line: int, character: int) -> Self:
        """Return position in pyparsing scheme from vscode scheme (lines starts from 0,
        columns starts from 0).
        """
        return cls(line + 1, character + 1)

    def to_lspt(self) -> lspt.Position:
        """Return position in pyparsing scheme from vscode scheme (lines starts from 1,
        columns starts from 1).
        """
        return lspt.Position(line=self.line - 1, character=self.column - 1)

    def offset(self, line: int, column: int) -> Self:
        """Create new Position offset by line and column."""
        return self.__class__(self.line + line, self.column + column)

    def __str__(self) -> str:
        return f"[line: {self.line}, col: {self.column}]"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line == __value.line and self.column == __value.column

    def __ne__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line != __value.line and self.column != __value.column

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line > __value.line or (
            self.line == __value.line and self.column > __value.column
        )

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line >= __value.line or (
            self.line == __value.line and self.column >= __value.column
        )

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line < __value.line or (
            self.line == __value.line and self.column < __value.column
        )

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return NotImplemented
        return self.line <= __value.line or (
            self.line == __value.line and self.column <= __value.column
        )
