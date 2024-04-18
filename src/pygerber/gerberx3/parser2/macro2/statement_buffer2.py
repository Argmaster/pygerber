"""Module contains class `StatementBuffer2 for macro statements."""

from __future__ import annotations

from typing import Iterator, List

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.gerberx3.parser2.macro2.statement2 import Statement2


class StatementBuffer2:
    """Buffer for macro statements."""

    def __init__(self) -> None:
        self.statements: list[Statement2] = []

    def add_statement(self, statement: Statement2) -> None:
        """Append a complete statement to the buffer."""
        self.statements.append(statement)

    def get_readonly(self) -> ReadonlyStatementBuffer2:
        """Return readonly buffer."""
        return ReadonlyStatementBuffer2(statements=self.statements)


class ReadonlyStatementBuffer2(FrozenGeneralModel):
    """Read-only macro statement buffer."""

    statements: List[Statement2]

    def __len__(self) -> int:
        """Return length of buffered commands."""
        return len(self.statements)

    def __iter__(self) -> Iterator[Statement2]:  # type: ignore[override]
        """Iterate over buffered draw commands."""
        yield from self.statements

    def __getitem__(self, position: int) -> Statement2:
        """Get draw command at position."""
        return self.statements[position]
