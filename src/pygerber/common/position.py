"""Contains tools for expressing positions in text."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self


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
